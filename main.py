import json
import sys
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from datetime import datetime
import argparse
plt.style.use('fivethirtyeight')

def convertTSToHour(data):
    ts = datetime.utcfromtimestamp(float(data)) #.strftime('%d%-1H')
    print(ts)
    #return ts

def buySellMACD(signal):
  buy = []
  sell = []
  lastBuy = []
  pnl = []
  buyPrice = np.nan
  flag = -1 #

  for i in range(0, len(signal)):
    if signal['MACD'][i] > signal['SignalLine'][i]:
      sell.append(np.nan)
      lastBuy.append(buyPrice)
      pnl.append(np.nan)

      if flag != 1:
        buy.append(signal['close'][i])
        flag = 1
        buyPrice = signal['close'][i]
      else:
        buy.append(np.nan)

    elif signal['MACD'][i] <= signal['SignalLine'][i]:
      buy.append(np.nan)
      lastBuy.append(buyPrice)  

      if flag != 0:
        sell.append(signal['close'][i])
        flag = 0
        pnl.append(float(signal['close'][i]) - float(buyPrice))
        buyPrice = np.nan
      else:
        sell.append(np.nan)
        pnl.append(np.nan)

    else:
      buy.append(np.nan)
      sell.append(np.nan)
      lastBuy.append(buyPrice)
      pnl.append(np.nan)

  return (buy, sell, lastBuy, pnl)

graphics=False

#parse parameters
parser = argparse.ArgumentParser()
parser.add_argument("-d", "--datafile", required=True)
parser.add_argument("-g", "--graphs", action='store_true')
args = parser.parse_args()
dataFile = args.datafile
graphics = args.graphs

print(dataFile)

with open(dataFile) as f:
    data = json.load(f)



df = pd.DataFrame.from_records(data)
#df.rename(columns = { '0': 'Betas', '1': 'P-values' }, inplace=True)
df.columns = ["open_time", "open", "high", "low", "close", "volume", "close_time", "volusd", "trades", "takerbase", "takerquote", 'ignore']

df['date'] = pd.to_datetime(df['open_time']/1000,unit='s')

df = df.set_index(pd.DatetimeIndex(df['date']))

print(df)

if graphics:
    plt.figure(figsize=(12.2, 4.5))
    plt.plot(df['close'], label='Close')
    plt.xticks(rotation=45)
    plt.title("Close price")
    plt.xlabel("Date")
    plt.ylabel("Price usd")
    plt.show()


shortEMA = df.close.ewm(span=12, adjust=False).mean()

longEMA = df.close.ewm(span=26, adjust=False).mean()

MACD = shortEMA - longEMA
signal = MACD.ewm(span=9, adjust=False).mean()

df['MACD'] = MACD
df['SignalLine'] = signal


if graphics:
    plt.figure(figsize=(12.2, 4.5))
    plt.xticks(rotation=45)
    plt.plot(df.index, MACD, label='MACD', color= 'blue')
    plt.plot(df.index, signal, label='Signal', color= 'red')
    plt.legend(loc='upper left')
    plt.show()


a = buySellMACD(df)
df['BuySignal'] = a[0]
df['SellSignal'] = a[1]
df['BuyPrice'] = a[2]
df['PnL'] = a[3]

print(df)

if graphics:
    plt.figure(figsize=(12.2, 5.5))
    plt.scatter(df.date, df['BuySignal'], color='green', label='Buy', marker='^', alpha=1)
    plt.scatter(df.date, df['SellSignal'], color='red', label='Sell', marker='v', alpha=1)
    #plt.plot(df['close'], label='Close', alpha=0.35)
    plt.title("buy and sell signal")
    plt.xticks(rotation=45)
    plt.xlabel('Date')
    plt.ylabel("Close")
    plt.legend(loc = 'upper left')
    plt.show()
