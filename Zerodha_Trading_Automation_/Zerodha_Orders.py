# -*- coding: utf-8 -*-
"""
Created on Sat Jul 30 11:59:47 2022

@author: HD
"""

def placeMarketOrder(symbol,buy_sell,quantity):    
    # Place an intraday market order on NSE
    if buy_sell == "buy":
        t_type=kite.TRANSACTION_TYPE_BUY
    elif buy_sell == "sell":
        t_type=kite.TRANSACTION_TYPE_SELL
    kite.place_order(tradingsymbol=symbol,
                    exchange=kite.EXCHANGE_NSE,
                    transaction_type=t_type,
                    quantity=quantity,
                    order_type=kite.ORDER_TYPE_MARKET,
                    product=kite.PRODUCT_MIS,
                    variety=kite.VARIETY_REGULAR)
    
def placeBracketOrder(symbol,buy_sell,quantity,atr,price):    
    # Place an intraday market order on NSE
    if buy_sell == "buy":
        t_type=kite.TRANSACTION_TYPE_BUY
    elif buy_sell == "sell":
        t_type=kite.TRANSACTION_TYPE_SELL
    kite.place_order(tradingsymbol=symbol,
                    exchange=kite.EXCHANGE_NSE,
                    transaction_type=t_type,
                    quantity=quantity,
                    order_type=kite.ORDER_TYPE_LIMIT,
                    price=price, #BO has to be a limit order, set a low price threshold
                    product=kite.PRODUCT_MIS,
                    variety=kite.VARIETY_BO,
                    squareoff=int(6*atr), 
                    stoploss=int(3*atr), 
                    trailing_stoploss=2)