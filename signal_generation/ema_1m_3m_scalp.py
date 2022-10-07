def scalp():
	
	""" This function detects 1 minute and 3 minute EMA scalp signals and writes them to 'signals' MySQL table """

	import make_binance_btc_ohlcv  # This is a dependency.  Main copy lives in ../data_acquisition
	import pandas as pd
	import pandas_ta as ta
	import numpy as np
	import sqlalchemy
	import pymysql
	from dotenv import load_dotenv
	import os
	import time
	from sqlalchemy import create_engine  
	import sys

	sys.path.append('/home/ubuntu/Trading_Bot_9000/data_transformation/')

	load_dotenv()
	
	host = os.getenv("HOST")
	dbname = os.getenv("DBNAME")
	username  = os.getenv("USERNAME")
	password = os.getenv("PASSWORD")     

	engine = create_engine(f"mysql+pymysql://{username}:{password}@{host}/{dbname}",)  
	conn = engine.connect()     
	
	# Read the signals table and get last timestamp from 1m and 3m data

	signal_df = pd.read_sql(f"SELECT * FROM signals", conn)
	signal_df.sort_values('timestamp')
	last_signal_1m = signal_df['ema_scalp_1m'].iloc[-1]
	last_signal_3m = signal_df['ema_scalp_3m'].iloc[-1]
	
	######## Run 1  minute OHCLV signals #################################################################################

	# Restructure dataframe with 1m data before running signal generator

	df = make_binance_btc_ohlcv.return_dataframe('1m')
	df.sort_values('Timestamp')
	df=df[df['Volume']!=0]
	df.isna().sum()
	df.reset_index(inplace=True)
	timestamp = df['Timestamp'].max()

	# Generate signal

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
	timestamp = df['Timestamp'].max()
	signal_1m = df['TotSignal'].iloc[-1] # Save 1m signal for conditional to decide whether to write to DB
	
	######## Run 3 minute OHCLV signals #################################################################################

	# Restructure dataframe with 3m data before running signal generator

	df = make_binance_btc_ohlcv.return_dataframe('3m')
	print(df)
	print('wtf')
	df=df[df['Volume']!=0]
	df.isna().sum()
	df.reset_index(inplace=True)


	# Generate signal

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

	# Get last 3m signal and 1m signal from DB and compare it to current signal
	# If current signal is != last signal, all current values are written into DB

	signal_3m = df['TotSignal'].iloc[-1]

	if (signal_1m != last_signal_1m) or (signal_3m != last_signal_3m):
	
		rint(timestamp)
		print(f'INSERT INTO signals (timestamp, price, ema_scalp_1m, ema_scalp_3m) VALUES ({timestamp},{close}, {signal_1m}, {signal_3m})')

		rs = conn.execute(f'INSERT INTO signals (timestamp, price, ema_scalp_1m, ema_scalp_3m) VALUES ({timestamp},{close}, {signal_1m}, {signal_3m})')
		
	print(timestamp)
	print('EMA 3m/1m ran successfully')
	print('')
