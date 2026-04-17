# -*- coding: utf-8 -*
"""
Created on Fri Sep 24 12:30:15 2021
@author: Aashish Rana

strategy = breakout of prvious day high(pdh) and previous day low(pdl)

entry logic  = long if current candle high is greater than pdh
               short if current candle low is lower than pdl
               
stop loss(fixed) = if long, sl will be pdl
                   if short, sl will be pdh
                   if sl didn't trigger, exit at 15:26'
"""


# import necessary liabraries
import pandas as pd

# importing daily data 
DF = pd.read_csv('E:\\COLLECIVE_DATA\\nifty_future_2011-2021\\nifty_future_daily.csv')

# importing 5 minute data 
DATA = pd.read_csv('E:\\COLLECIVE_DATA\\nifty_future_2011-2021\\nifty_future_5m.csv')

# for storing the signal
SIGNAL = [0] * len(DATA)

# set boolen to false initially
BUY = False
SELL = False

#made a start variable so that i can use it to jump to next day
START = 75

#count the number of trades
COUNT = 0

#i will record every trade in this trade log 
trade_log = pd.DataFrame(['Entry_date','Exit_date'])

'''i have made a loop which will extract high and low of the previous day from daily data and then there is second loop inside the first loop to generate signal on current day in 5 minutes data by taking into consideration the pdh and pdl from daily data.'''

for i in range(len(DF)):
    for j in range(START,len(DATA)):
            if (BUY == False and DATA['High'][j] > DF['High'][i] and 
                SELL == False):
                SIGNAL[j] = 1
                BUY = True
                COUNT += 1
                entry_price = DATA['High'][j].astype(float)
                entry_price_a_cost = entry_price+(entry_price*0.0001)
                trade_log =trade_log.append({'Type':'Long',
                                           'Entry_date':DATA['Datetime'][j],
                                           'Entry_price':entry_price,
                                           'entry_price_a_cost':entry_price_a_cost},
                                           ignore_index=True)
                
            if (BUY == True):
                if (DATA['Low'][j] < DF['Low'][i] or 
                    ('15:26' in DATA['Datetime'][j])):
                    SIGNAL[j] = 2
                    START += 75
                    BUY = False
                    exit_price = DATA['Low'][j].astype(float)
                    exit_price_a_cost = exit_price-(exit_price*0.0001)
                    points =exit_price_a_cost-entry_price_a_cost
                    returns = (exit_price_a_cost/entry_price_a_cost)-1
                    trade_log =trade_log.append({'Exit_date':DATA['Datetime'][j],
                                               'Exit_price':exit_price,
                                               'exit_price_a_cost':exit_price_a_cost,
                                               'points':points,
                                               'returns': returns},
                                               ignore_index = True)
                    break
                    
            if (SELL == False and DATA['Low'][j] < DF['Low'][i] and 
                BUY == False):
                SIGNAL[j] = 1
                SELL = True
                COUNT += 1
                entry_price = DATA['Low'][j].astype(float)
                entry_price_a_cost = entry_price-(entry_price*0.0001)
                trade_log =trade_log.append({'Type':'Short',
                                            'Entry_date':DATA['Datetime'][j],
                                           'Entry_price':entry_price,
                                           'entry_price_a_cost':entry_price_a_cost},
                                           ignore_index=True)
                
            if (SELL == True):
                if (DATA['High'][j] > DF['High'][i] or 
                    ('15:26' in DATA['Datetime'][j])):
                    SIGNAL[j] = 2
                    START += 75
                    SELL = False
                    exit_price = DATA['High'][j].astype(float)
                    exit_price_a_cost = exit_price+(exit_price*0.0001)
                    points = entry_price_a_cost-exit_price_a_cost
                    returns = (entry_price_a_cost/exit_price_a_cost)-1
                    trade_log =trade_log.append({'Exit_date':DATA['Datetime'][j],
                                               'Exit_price':exit_price,
                                               'exit_price_a_cost':exit_price_a_cost,
                                               'points':points,
                                               'returns':returns},
                                               ignore_index = True)
                    break 
            
            if '15:26' in DATA['Datetime'][j]:
                START += 75
                break
                
    
DATA['Signal']= SIGNAL
print(COUNT)
#COUNT = 2373

# shifting the rows to up in trade log 
trade_log[['Exit_date','Exit_price','exit_price_a_cost','points','returns']]=trade_log [['Exit_date','Exit_price','exit_price_a_cost','points','returns']].shift(-1)

#dropping the column label with 0
trade_log.drop([0],axis=1,inplace=True)

#dropping all nan values
trade_log.dropna(inplace=True)

#resetting index
trade_log.reset_index(inplace=True,drop=True)



#saving_trade_log
trade_log.to_excel('breakout_pdh_pdl_trade_log.xlsx',sheet_name='main')

DATA.to_excel('breakout_pdh_pdl_updated.xlsx',sheet_name='main')

