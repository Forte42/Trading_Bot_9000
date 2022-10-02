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

	df = pd.read_sql(f"SELECT * FROM binance_btc_trades ORDER BY id DESC LIMIT 300", conn)   
	df['lastprice'] = df['price'].shift(1).astype(float)
	
	df=df[df['qty']!=0]
	df.isna().sum()
	df.reset_index(inplace=True)

	df["EMA50"] = ta.ema(df.price, length=100)
	df["EMA100"] = ta.ema(df.price, length=200)
	df["EMA150"] = ta.ema(df.price, length=300)

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
	
	df=df.reindex(index=df.index[::-1])	
	df['price'] = df['price'].astype(float)
	df['lastprice'] = df['lastprice'].astype(float)	
	for row in range(0, len(df)):
		
	
		TotSignal[row] = 0
		if df.EMAsignal[row]==1 and df.lastprice[row]>df.EMA50[row] and df.price[row]<df.EMA50[row]:
			TotSignal[row]=1 #signal to short the ticker
		if df.EMAsignal[row]==2 and df.lastprice[row]<df.EMA50[row] and df.price[row]>df.EMA50[row]:
			TotSignal[row]=2 #signal to long the ticker

	import time
	time.sleep(.1)
	df['TotSignal']=TotSignal
	#	print(df[['TotSignal', 'price', 'lastprice']])
	print(df)
	current_signal = df['TotSignal'].iloc[-1]
	rs = conn.execute(f'UPDATE signals SET ema_scalp_0m={current_signal} WHERE anchor=1')
	#if current_signal > 0:
	#	print('found one')
	#	print(current_signal)
	#	quit()


