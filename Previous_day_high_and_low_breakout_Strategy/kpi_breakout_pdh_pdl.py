# -*- coding: utf-8 -*
"""
Created on Fri Sep 24 12:30:15 2021
@author: Aashish Rana

kpi =  only returns and points        
        
strategy = breakout of prvious day high(pdh) and previous day low(pdl)

entry logic  = long if current candle high is greater than pdh
               short if current candle low is lower than pdl
               
stop loss(fixed) = if long, sl will be pdl
                   if short, sl will be pdh
                   if sl didn't trigger, exit at 15:26'
"""

# import necessary liabraries
import pandas as pd
import numpy as np
from openpyxl import load_workbook
import matplotlib.pyplot as plt

# read the trade log file
df = pd.read_excel('E:\\breakout_pdh_pdl\\breakout_pdh_pdl_trade_log.xlsx',sheet_name='main',parse_dates =['Entry_date'],index_col = 'Entry_date')

# group the trade log points annually
Annual_points = df.groupby(pd.Grouper(freq = 'Y'))['points','returns'].sum()

#saving the annual points and returns to existing file which is trade_log
path = 'E:\\breakout_pdh_pdl\\breakout_pdh_pdl_trade_log.xlsx'
book = load_workbook(path)
writer = pd.ExcelWriter(path,engine = 'openpyxl')
writer.book = book
Annual_points.to_excel(writer,sheet_name = 'points and returns')
writer.save()
writer.close()

Annual_points.to_excel('breakout_pdh_pdl_trade_log.xlsx',sheet_name = 'points and returns')


# group the trade log points annually
Annual_points = df.groupby(pd.Grouper(freq = 'Y'))['points'].sum()

# plotting the charts of annual points 
Annual_points.plot(kind = 'bar',xlabel = 'year',ylabel = 'points',figsize = (9,3),title = 'NIFTY FUTURES')
