import sys
from collections import defaultdict
from datetime import datetime

import pandas as pd

sys.path.append("/home/aashish/repos/auto-journal/metrics")

from metrics import apply_all_metrics


def process_journal(input_csv, output_csv, metrics_txt_file):
    """
    Processes a trading journal from an input CSV file, calculates metrics, and saves the results to an output CSV file and a metrics text file.

    Parameters:
    input_csv (str): Path to the input CSV file containing trade data.
    output_csv (str): Path to the output CSV file where processed data will be saved.
    metrics_txt_file (str): Path to the text file where calculated metrics will be saved.

    Returns:
    pd.DataFrame: A DataFrame containing the processed trade data with calculated metrics.
    """

    df = pd.read_csv(input_csv)
    df["order_execution_time"] = pd.to_datetime(df["order_execution_time"])

    trades = defaultdict(
        lambda: {
            "symbol": "",
            "buys": defaultdict(
                lambda: {"quantity": 0, "total_price": 0, "order_execution_time": None}
            ),
            "sells": defaultdict(
                lambda: {"quantity": 0, "total_price": 0, "order_execution_time": None}
            ),
        }
    )

    for _, row in df.iterrows():
        symbol = row["symbol"]
        trade_type = row["trade_type"]
        quantity = int(row["quantity"])
        price = float(row["price"])
        order_id = row["order_id"]
        order_execution_time = row["order_execution_time"]

        trades[symbol]["symbol"] = symbol

        if trade_type == "buy":
            trades[symbol]["buys"][order_id]["quantity"] += quantity
            trades[symbol]["buys"][order_id]["total_price"] += quantity * price
            trades[symbol]["buys"][order_id][
                "order_execution_time"
            ] = order_execution_time
        else:
            trades[symbol]["sells"][order_id]["quantity"] += quantity
            trades[symbol]["sells"][order_id]["total_price"] += quantity * price
            trades[symbol]["sells"][order_id][
                "order_execution_time"
            ] = order_execution_time

    data = []
    for symbol_data in trades.values():
        symbol = symbol_data["symbol"]
        buys = symbol_data["buys"]
        sells = symbol_data["sells"]

        buy_quantity = sum(trade["quantity"] for trade in buys.values())
        sell_quantity = sum(trade["quantity"] for trade in sells.values())

        avg_buy_price = (
            sum(trade["total_price"] for trade in buys.values()) / buy_quantity
            if buy_quantity > 0
            else 0
        )
        avg_sell_price = (
            sum(trade["total_price"] for trade in sells.values()) / sell_quantity
            if sell_quantity > 0
            else 0
        )

        buy_time = min(
            (trade["order_execution_time"] for trade in buys.values()), default=None
        )
        sell_time = max(
            (trade["order_execution_time"] for trade in sells.values()), default=None
        )

        latest_time = max(buy_time, sell_time) if sell_time else buy_time

        data.append(
            {
                "symbol": symbol,
                "buy_quantity": buy_quantity,
                "avg_buy_price": round(avg_buy_price, 2),
                "buy_time": buy_time,
                "sell_quantity": sell_quantity,
                "avg_sell_price": round(avg_sell_price, 2),
                "sell_time": sell_time,
                "latest_time": latest_time,
            }
        )

    result_df = pd.DataFrame(data)

    # Sort the DataFrame by the latest time, most recent first
    result_df = result_df.sort_values("latest_time", ascending=False)

    metrics, result_df = apply_all_metrics(result_df)

    # Save the DataFrame to the output CSV file
    result_df.to_csv(output_csv, index=False)

    with open(metrics_txt_file, "w") as file:
        for key, value in metrics.items():
            file.write(f"{key}: {value}\n")

    return result_df


# Example usage:
input_file = "data/tradebook-XZ8318-EQ.csv"
current_date = datetime.now().strftime("%Y-%m-%d")
output_csv_file = f"data/processed_journal_{current_date}.csv"
metrics_txt_file = f"data/processed_journal_metrics{current_date}.txt"

process_journal(input_file, output_csv_file, metrics_txt_file)
