import pandas as pd
from alpha_vantage.timeseries import TimeSeries
from yahoo_fin import stock_info as si
import configparser
import numpy as np
import stratergy

config = configparser.ConfigParser()
config.read('.cfg')
api_key = config['api']['api_key']

def get_stocks():
    arr = []
    gainers = si.get_day_gainers().head(5)
    tickers = gainers.Symbol
    for i in tickers:
        arr.append(i)
    return arr

arr = []
for i in get_stocks():
    opt  = stratergy.optimal_strat(i)
    print(opt)
    arr.append(opt)

value = 0
for i in arr:
    value += 200*(1+i[1])

print(value)

print(get_stocks())