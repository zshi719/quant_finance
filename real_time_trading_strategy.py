#!/bin/python3

"""
Real time trading strategy
"""
"""
Use the linear regression to predict the price for tomorrow.
"""
import numpy as np
import pandas as pd
import yfinance as yf
from pandas_datareader import data

yf.pdr_override()
from sklearn.linear_model import LinearRegression


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

market_data = []
lr = None


def onMarketDataUpdate(mkdata):
    global lr
    # print(mkdata)
    global market_data
    print(mkdata['Close'], mkdata['Volume'], mkdata['High'] - mkdata['Low'])
    market_data.append(mkdata)
    if len(market_data) == 1000:  # getting the historical data
        data_df = pd.DataFrame(market_data)
        data_df['High_Low'] = data_df['High'] - data_df['Low']
        X = data_df[['Close', 'Volume', 'High_Low']]
        Y = data_df['Close'].shift(-1)

        # Drop rows with missing values
        X.dropna(inplace=True)
        Y.dropna(inplace=True)
        lr = LinearRegression()
        lr.fit(X[1:], Y)
    if len(market_data) > 1000:  # Predicting once the model is created
        predicted_tomorrow_close = \
        lr.predict(np.array([row['Close'], row['Volume'], row['High'] - row['Low']]).reshape(1, -1))[0]
        # print('predicted_price',predicted_tomorrow_close)
        # print('current_price',row['Close'])
        if (row['Close'] < predicted_tomorrow_close):
            print('Buy')
        else:
            print('Sell')


for i, row in goog_data.iterrows():
    onMarketDataUpdate(row)
