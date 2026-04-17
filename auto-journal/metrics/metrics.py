import numpy as np
import pandas as pd


def calculate_profit_loss(df):
    """
    Calculate profit/loss for each trade.
    Assumes 'buy_quantity', 'avg_buy_price', 'sell_quantity', 'avg_sell_price' columns exist.
    """
    df["profit_loss"] = (df["avg_sell_price"] - df["avg_buy_price"]) * np.minimum(
        df["buy_quantity"], df["sell_quantity"]
    )
    return df


def calculate_roi(df):
    """
    Calculate Return on Investment (ROI) for each trade.
    """
    df["roi"] = (df["avg_sell_price"] - df["avg_buy_price"]) / df["avg_buy_price"] * 100
    return df


def calculate_win_loss_ratio(df):
    """
    Calculate the win/loss ratio across all trades.
    """
    winning_trades = (df["profit_loss"] > 0).sum()
    losing_trades = (df["profit_loss"] < 0).sum()
    win_loss_ratio = winning_trades / losing_trades if losing_trades > 0 else np.inf
    return win_loss_ratio


def calculate_average_profit_per_trade(df):
    """
    Calculate the average profit per trade.
    """
    return df["profit_loss"].mean()


def calculate_average_holding_period(df):
    """
    Calculate the average holding period for trades.
    Assumes 'buy_time' and 'sell_time' columns exist and are in datetime format.
    """
    df["holding_period"] = (df["sell_time"] - df["buy_time"]).dt.total_seconds() / (
        3600 * 24
    )  # in days
    return df["holding_period"].mean()


def apply_all_metrics(df):
    """
    Apply all metrics to the DataFrame and return a summary dictionary.
    """
    df = calculate_profit_loss(df)
    df = calculate_roi(df)

    metrics = {
        "win_loss_ratio": calculate_win_loss_ratio(df),
        "average_profit_per_trade": calculate_average_profit_per_trade(df),
        "average_holding_period": calculate_average_holding_period(df),
    }

    return metrics, df
