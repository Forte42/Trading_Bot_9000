import talib #comment out this line to run without talib dependency
import sqlalchemy
from sqlalchemy import create_engine
import pymysql
import time
import datetime
import pandas as pd
import numpy as np
import pandas_ta as pta #use pip install pandas_ta
from dotenv import load_dotenv
import os

pd.set_option("display.max_rows", None, "display.max_columns", None)

load_dotenv()
host = os.getenv("HOST")
dbname = os.getenv("DBNAME")
username = os.getenv("USERNAME")
password = os.getenv("PASSWORD")

engine = create_engine(f"mysql+pymysql://{username}:{password}@{host}/{dbname}",)

while True:
	
	conn = engine.connect()
	df = pd.read_sql("SELECT * FROM binance_btc_0m ORDER BY id DESC LIMIT 2500", conn)
	df = df[['id','time','price','qty', 'isBestMatch']]
	df['price'] = df['price'].astype(float)
	df['OBV'] = talib.OBV(df['price'], df['qty'])
	df['OBV2000MA']= df['OBV'].rolling(2000).mean() 
	df['DIFF'] = df['OBV'] - df['OBV2000MA']
	df = df[['price', 'OBV', 'OBV2000MA', 'DIFF']]
	df['CHG_From_2K_Ago'] = df['price'] - df['price'].shift(2000)
	df['CHG/OBV'] = df['CHG_From_2K_Ago'] / df['OBV']
	print(df.tail(25))
	conn.close()



#df_1m = pd.read_sql(f"SELECT * FROM binance_btc_1m", conn)
#df_1m = df_1m[['Timestamp','Open','High','Low', 'Close', 'Volume', 'Number_Of_Trades']]
#df_1m['Close'] = df_1m['Close'].astype(float)
#df_1m['Change'] = df_1m['Close'] - df_1m['Close'].shift(1)
#df_1m['OBV_1m'] = talib.OBV(df_1m['Close'], df_1m['Volume'])
##print(df_1m)
#
#df_3m = pd.read_sql(f"SELECT * FROM binance_btc_3m", conn)
#df_3m = df_3m[['Timestamp','Open','High','Low', 'Close', 'Volume', 'Number_Of_Trades']]
#df_3m['Close'] = df_3m['Close'].astype(float)
#df_3m['Change'] = df_3m['Close'] - df_3m['Close'].shift(1)
#df_3m['OBV_3m'] = talib.OBV(df_3m['Close'], df_3m['Volume'])
##print(df_3m)
#
#backrollingN = 10
#df_1m['slopeOBV_1m'] = df_1m['OBV_1m'].diff(periods=1)
#df_1m['slopeOBV_1m'] = df_1m['slopeOBV_1m'].rolling(window=backrollingN).mean()
#
#backrollingN = 10
#df_3m['slopeOBV_3m'] = df_3m['OBV_3m'].diff(periods=1)
#df_3m['slopeOBV_3m'] = df_3m['slopeOBV_3m'].rolling(window=backrollingN).mean()
#
#
#print(df_1m.tail(20)) #[['Change', 'slopeOBV']])
#print(df_3m.tail(20))
