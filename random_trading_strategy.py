#!/bin/python3

"""
Random trading strategy

Create a trading strategy getting random positions.
Use the trading ecosystem described in class with the excel spreadsheet to determine the pnl with the cash 
and the holding at any time
"""


import pandas as pd
import numpy as np
from pandas_datareader import data
import yfinance as yf
import matplotlib.pyplot as plt

yf.pdr_override()


def load_financial_data(start_date, end_date, output_file):
    try:
        df = pd.read_pickle(output_file)
        print('File data found...reading GOOG data')
    except FileNotFoundError:
        print('File not found...downloading the GOOG data')
        df = data.DataReader('GOOG', start_date, end_date)
        df.to_pickle(output_file)
    return df


goog_data = load_financial_data(start_date='2001-01-01',
                                end_date='2018-01-01',
                                output_file='goog_data.pkl')

import random

random.seed(6666)


def random_data(financial_data, short_window, long_window):
    signals = pd.DataFrame(index=financial_data.index)
    # data = np.random.randint(0, 2, size=financial_data.shape[0])
    data = np.ones(financial_data.shape[0])
    data[0] = 0
    data[financial_data.shape[0] - 1] = 0

    signals['signal'] = data  # position
    # 00000011111111110000000000 # position
    # 000000100000000-1000000000 # orders
    signals['orders'] = signals['signal'].diff()  # orders
    return signals


import numpy as np


def ma_strategy_data(financial_data, short_window, long_window):
    signals = pd.DataFrame(index=financial_data.index)
    signals['small_ma'] = financial_data['Adj Close'].rolling(short_window).mean()
    signals['long_ma'] = financial_data['Adj Close'].rolling(long_window).mean()
    signals['signal'] = np.where(signals['small_ma'] > signals['long_ma'],
                                 1.0, 0.0)
    signals['orders'] = signals['signal'].diff()  # orders
    return signals


ts = random_data(goog_data, 20, 100)
signals = ts
fig = plt.figure()
ax1 = fig.add_subplot(111, ylabel='Google price in $')
goog_data["Adj Close"].plot(ax=ax1, color='g', lw=.5)

ax1.plot(ts.loc[ts.orders == 1.0].index,
         goog_data["Adj Close"][ts.orders == 1.0],
         '^', markersize=7, color='k')

ax1.plot(ts.loc[ts.orders == -1.0].index,
         goog_data["Adj Close"][ts.orders == -1.0],
         'v', markersize=7, color='k')

plt.legend(["Price", "Short mavg", "Long mavg", "Buy", "Sell"])
plt.title("Random Trading Strategy")

plt.show()

# set your initial amount of money you want
# to invest --- here it is 10,000
initial_capital = float(10000.0)

# create a new dataframe positions
positions = pd.DataFrame(index=signals.index).fillna(0.0)

# buy 10 shares of MSFT when signal is 1 and sell 10 shares of MSFT when signal is -1
# assign these values to the column MSFT of the dataframe positions
positions['GOOG'] = 10 * ts['signal']

# calculate the notional (quantity x price) and store it into the variable portfolio
portfolio = positions.multiply(goog_data['Adj Close'], axis=0)

# Add `holdings` to portfolio
portfolio['holdings'] = (positions.multiply(goog_data['Adj Close'], axis=0)).sum(axis=1)


pos_diff = positions.diff()
portfolio['cash'] = initial_capital - (pos_diff.multiply(goog_data['Adj Close'], axis=0)).sum(axis=1).cumsum()

portfolio['total'] = portfolio['cash'] + portfolio['holdings']

portfolio['returns'] = portfolio['total'].pct_change()

print(portfolio)

# portfolio['holdings'].plot( color='g', lw=.5)
portfolio['cash'].plot(color='r', lw=.5)
portfolio['total'].plot(color='g', lw=.5)
plt.title("Random Trading Strategy")
plt.legend()
plt.show()
