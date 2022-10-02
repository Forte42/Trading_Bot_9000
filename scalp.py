import make_binance_btc_ohlcv
import pandas as pd
import pandas_ta as ta
import numpy as np
import sqlalchemy
import pymysql
from dotenv import load_dotenv
import os
import time
from sqlalchemy import create_engine  


load_dotenv()

host = os.getenv("HOST")                                                                                                                                      
dbname = os.getenv("DBNAME")                                                                                                                                  
username = os.getenv("USERNAME")                                                                                                                              
password = os.getenv("PASSWORD")     

engine = create_engine(f"mysql+pymysql://{username}:{password}@{host}/{dbname}",)  

conn = engine.connect()     

while True:

	df = make_binance_btc_ohlcv.return_dataframe('1m')

	df.sort_values('Timestamp')
	df=df[df['Volume']!=0]
	df.isna().sum()
	df.reset_index(inplace=True)

	df["EMA50"] = ta.ema(df.Close, length=50)
	df["EMA100"] = ta.ema(df.Close, length=100)
	df["EMA150"] = ta.ema(df.Close, length=150)

	backrollingN = 10
	df['slopeEMA50'] = df['EMA50'].diff(periods=1)
	df['slopeEMA50'] = df['slopeEMA50'].rolling(window=backrollingN).mean()

	df['slopeEMA100'] = df['EMA100'].diff(periods=1)
	df['slopeEMA100'] = df['slopeEMA100'].rolling(window=backrollingN).mean()

	df['slopeEMA150'] = df['EMA150'].diff(periods=1)
	df['slopeEMA150'] = df['slopeEMA150'].rolling(window=backrollingN).mean()

	conditions = [
	    ( (df['EMA50']<df['EMA100']) & (df['EMA100']<df['EMA150']) & (df['slopeEMA50']<0) & (df['slopeEMA100']<0) & (df['slopeEMA150']<0) ),   #downtrend =1
	    ( (df['EMA50']>df['EMA100']) & (df['EMA100']>df['EMA150']) & (df['slopeEMA50']>0) & (df['slopeEMA100']>0) & (df['slopeEMA150']>0) )    #uptrend = 2
		   ]
	choices = [1, 2]
	df['EMAsignal'] = np.select(conditions, choices, default=0)

	TotSignal = [0] * len(df)
	
	for row in range(0, len(df)):
		
		TotSignal[row] = 0
		if df.EMAsignal[row]==1 and df.Open[row]>df.EMA50[row] and df.Close[row]<df.EMA50[row]:
			TotSignal[row]=1 #signal to short the ticker
		if df.EMAsignal[row]==2 and df.Open[row]<df.EMA50[row] and df.Close[row]>df.EMA50[row]:
			TotSignal[row]=2 #signal to long the ticker

	df['TotSignal']=TotSignal

	print(df["TotSignal"].value_counts())

	print (df.tail())

	current_signal = df['TotSignal'].iloc[-1]
	rs = conn.execute(f'UPDATE signals SET ema_scalp_1m={current_signal} WHERE anchor=1')

	#####################################################################################################################

	df = make_binance_btc_ohlcv.return_dataframe('3m')
	print(df)
	df=df[df['Volume']!=0]
	df.isna().sum()
	df.reset_index(inplace=True)

	df["EMA50"] = ta.ema(df.Close, length=50)
	df["EMA100"] = ta.ema(df.Close, length=100)
	df["EMA150"] = ta.ema(df.Close, length=150)

	backrollingN = 10
	df['slopeEMA50'] = df['EMA50'].diff(periods=1)
	df['slopeEMA50'] = df['slopeEMA50'].rolling(window=backrollingN).mean()

	df['slopeEMA100'] = df['EMA100'].diff(periods=1)
	df['slopeEMA100'] = df['slopeEMA100'].rolling(window=backrollingN).mean()

	df['slopeEMA150'] = df['EMA150'].diff(periods=1)
	df['slopeEMA150'] = df['slopeEMA150'].rolling(window=backrollingN).mean()

	conditions = [
	    ( (df['EMA50']<df['EMA100']) & (df['EMA100']<df['EMA150']) & (df['slopeEMA50']<0) & (df['slopeEMA100']<0) & (df['slopeEMA150']<0) ),   #downtrend =1
	    ( (df['EMA50']>df['EMA100']) & (df['EMA100']>df['EMA150']) & (df['slopeEMA50']>0) & (df['slopeEMA100']>0) & (df['slopeEMA150']>0) )    #uptrend = 2
		   ]
	choices = [1, 2]
	df['EMAsignal'] = np.select(conditions, choices, default=0)

	TotSignal = [0] * len(df)
	for row in range(0, len(df)):
		
		TotSignal[row] = 0
		if df.EMAsignal[row]==1 and df.Open[row]>df.EMA50[row] and df.Close[row]<df.EMA50[row]:
			TotSignal[row]=1 #signal to short the ticker
		if df.EMAsignal[row]==2 and df.Open[row]<df.EMA50[row] and df.Close[row]>df.EMA50[row]:
			TotSignal[row]=2 #signal to long the ticker

	df['TotSignal']=TotSignal

	current_signal = df['TotSignal'].iloc[-1]
	rs = conn.execute(f'UPDATE signals SET ema_scalp_3m={current_signal} WHERE anchor=1')
	time.sleep(.5)
