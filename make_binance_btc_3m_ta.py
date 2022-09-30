import talib #comment out this line to run without talib dependency
import sqlalchemy
from sqlalchemy import create_engine
import pymysql
import time
import datetime
import pandas as pd
import numpy as np
import pandas_ta as pta

engine = create_engine("mysql+pymysql://admin:52GxbFuetNqvFn@crypto-db.cb84pseap2n8.us-east-1.rds.amazonaws.com:3306/crypto",)

conn = engine.connect()

df = pd.read_sql("SELECT * FROM binance_btc_3m", conn)

df.drop('TBB', axis = 1, inplace=True)
df.drop('TBQ', axis = 1, inplace=True)
df.drop('NOT_APPLICABLE', axis = 1, inplace=True)
df.drop('Close_Timestamp', axis = 1, inplace=True)
df.drop('QAV', axis = 1, inplace=True)
#df['Timestamp'] = df['Timestamp'].astype(datetime)
df['Open'] = df['Open'].astype(float).astype(float).round(4)
df['High'] = df['High'].astype(float).astype(float).round(4)
df['Low'] = df['Low'].astype(float).astype(float).round(4)
df['Close'] = df['Close'].astype(float).astype(float).round(4)
df['Volume'] = df['Volume'].astype(float).astype(float).round(2)


df['Prev_Close'] = df['Close'].shift(1)
df['Bar_Change'] = df['Close'] - df['Prev_Close']
df['Intrabar_Change'] = df['Close'] - df['Open']

df['Bar_Range'] = df['High'] - df['Low']

df['Updown'] = 3
df.loc[df['Bar_Change'] > 0, 'Updown'] = 1
df.loc[df['Bar_Change'] < 0, 'Updown'] = 0

df['Iupdown'] = 3
df.loc[df['Intrabar_Change'] > 0, 'Iupdown'] = 1
df.loc[df['Intrabar_Change'] < 0, 'Iupdown'] = 0
df['Iconsecutive'] = df['Iupdown'].groupby((df['Iupdown'] != df['Iupdown'].shift()).cumsum()).cumcount() + 1

df['10MA'] = df['Close'].rolling(10).mean().astype(float).round(2)
df['50MA'] = df['Close'].rolling(50).mean().astype(float).round(2)
df['200MA'] = df['Close'].rolling(200).mean().astype(float).round(2)
df['10MAV'] = df['Volume'].rolling(10).mean().astype(float).round(2)
df['50MAV'] = df['Volume'].rolling(50).mean().astype(float).round(2)
df['200MAV'] = df['Volume'].rolling(200).mean().astype(float).round(2)

df['RSI'] = pta.rsi(df['Close'], length = 14).astype(float).round(2) #uses pandas-ta rsi function
df['RSI'] = df['RSI'].astype(float).round(2)
df['MACD'] = (talib.EMA(df['Close'], 13))-(talib.EMA(df['Close'], 26)).astype(float).round(2).astype(float).round(2) #comment out this line to run without talib dependency
df['VWAP'] = (np.cumsum(df.Volume * df.Close) / np.cumsum(df.Volume)).astype(float).round(2).astype(float).round(2)


# Candlestick Components
# these are used to describe individual candlesticks

# Upper shadow absolute value
df['USA'] = df['High'] - df[['Open','Close']].max(axis=1).astype(float).round(4)

# Lower shadow absolute value
df['LSA'] = (df[['Open','Close']].min(axis=1) - df['Low']).astype(float).round(4)

# Candle body absolute value
df['BODYA'] = (df[['Open','Close']].max(axis=1) - df[['Open','Close']].min(axis=1)).astype(float).round(4)

# Ratio of lower shadow to upper shadow
df['LUR'] = (df['LSA'] / df['USA']).astype(float).round(4)

# Ratio of upper shadow to lower shadow
df['ULR'] = (df['USA'] / df['LSA']).astype(float).round(4)

# Lower shadow as ratio to bar range
df['LSRR'] = ((df['High'] - df[['Open','Close']].max(axis=1)) / df['Bar_Range']).astype(float).round(4)

# Upper shadow as ratio to bar range
df['USRR'] = ((df[['Open' , 'Close']].min(axis=1) - df['Low']) / df['Bar_Range']).astype(float).round(4)

# Candlebody ratio to range
df['BODYRR'] = 1 - (df['USRR'] + df['LSRR']).astype(float).round(4)

# Ratio of open to close

df['OCR'] = df[['Open','Close']].min(axis=1) / df[['Open','Close']].max(axis=1).astype(float).round(4)

# Is this candle XXXXX doji?

df['Dragonfly'] = 0
df.loc[(df['OCR'] > .9985) & (df['USRR'] > .905), 'Dragonfly'] = 1

df['Gravestone'] = 0
df.loc[(df['OCR'] > .9985) & (df['USRR'] < .095), 'Gravestone'] = 1

df['Green_Marubozu'] = 0
df.loc[(df['USRR'] < .01) & (df['LSRR'] < .01) & (df['Iupdown'] == 1), "Green_Marubozu"] = 1

df['Red_Marubozu'] = 0
df.loc[(df['USRR'] < .01) & (df['LSRR'] < .01) & (df['Iupdown'] == 0), "Red_Marubozu"] = 1

df['Shooting_Star'] = 0
df.loc[(df['USRR'] < .04) & (df['LSRR'] > .75) & (df['Iupdown'] == 0) & (df['Iupdown'] == 0) & (df['OCR'] <= .9985), "Shooting_Star"]

df['Hanging_Man'] = 0
df.loc[(df['USRR'] < .75) & (df['LSRR'] < .04) & (df['Iupdown'] == 0) & (df['Iupdown'] == 0) & (df['OCR'] <= .9985), "Shooting_Star"]

df['Hammer'] = 0    
df.loc[(df['USRR'] > .75) & (df['LSRR'] < .04 ) & (df['Iupdown'] == 1) & (df['OCR'] <= .9985), "Hammer"] = 1

df['Inverted_Hammer'] = 0
df.loc[(df['USRR'] < .04) & (df['LSRR'] > .75 ) & (df['Iupdown'] == 1) & (df['OCR'] <= .9985), "Inverted_Hammer"] = 1

df['Doji'] = 0
df.loc[(df['OCR'] > .9985) ,"Doji"] = 1

df['Doji_Star'] = 0
df.loc[((df['LSA'] / df['USA']) > .9996) & (df['LSA'] / df['USA'] < 1.004) & (df['OCR'] > .9985) ,"Doji_Star"] = 1

# Drop candlestick descriptor components

df.drop('OCR', axis=1, inplace = True)
df.drop('BODYRR', axis=1, inplace = True)
df.drop('USRR', axis=1, inplace = True)
df.drop('LSA', axis=1, inplace = True)
df.drop('USA', axis=1, inplace = True)
df.drop('LSRR', axis=1, inplace = True)
df.drop('ULR', axis=1, inplace = True)
df.drop('LUR', axis=1, inplace = True)
df.drop('BODYA', axis=1, inplace = True)


print(df.tail(20))

#result = df[df.Iupdown > 2]
#print(result)
