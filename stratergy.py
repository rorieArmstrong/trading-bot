# Choose the best stratergy 

import pandas as pd
from alpha_vantage.timeseries import TimeSeries
from yahoo_fin import stock_info as si
import configparser
import numpy as np

config = configparser.ConfigParser()
config.read('.cfg')
api_key = config['api']['api_key']

def optimal_strat(ticker):
    opt_strat = 15
    returns = []
    ts = TimeSeries(key=api_key, output_format='pandas')
    data, meta_data = ts.get_intraday(ticker, interval='1min', outputsize='full')

    data['returns'] = np.log(data['4. close'] / data['4. close'].shift(1)) 
    cols = []

    for momentum in [15, 30, 60, 120]:
        col = 'position_' + str(momentum)
        data[col] = np.sign(data['returns'].rolling(momentum).mean()) 
        cols.append(col)

    strats = ['returns']  
    stock_return = data.returns.sum()

    for col in cols:  
        strat = 'strategy_' + str(col.split('_')[1])
        data[strat] = data[col].shift(1) * data['returns']  
        strats.append(strat)
        returns.append(data[strat].sum())

    x = returns.index(max(returns))
    return opt_strat*(2**x), max(returns)