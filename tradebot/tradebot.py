import pandas as pd
import numpy as np
from dotenv import load_dotenv
import os
import requests
import datetime
from sqlalchemy import create_engine
import pymysql
import sqlalchemy
import make_binance_btc_ohlcv
import time
import order_functions

while True:
	
	engine = create_engine(f"mysql+pymysql://{username}:{password}@{host}/{dbname}",)               
	conn = engine.connect()  
	
	df = {}
	df = pd.read_sql(f"SELECT ema_scalp_1m FROM signals order by tIMESTAMP desc LIMIT 1", conn) 
	signal_1m = df['ema_scalp_1m'].iloc[-1].astype(int)
	print(signal_1m)
	df2 = {}
	df2 = pd.read_sql(f"SELECT ema_scalp_3m FROM signals ORDER BY Timestamp DESC LIMIT 1", conn)
	signal_3m = df2['ema_scalp_3m'].iloc[-1].astype(int)
	print(signal_3m)
	df3 = {}
	df3 = pd.read_sql(f"SELECT timestamp, value FROM lstm_3m_signal ORDER BY timestamp DESC LIMIT 1", conn)
	lstm_prediction = df3['value'].iloc[-1].astype(float)
	print(lstm_prediction)
	df4 = {}
	df4 = make_binance_btc_ohlcv.return_dataframe('3m')
	atr = df4['ATR'].iloc[-1].astype(float)
	print(atr) 

	df5 = {}
	df5 = pd.read_sql('select * from binance_btc_trades order by id desc limit 1;', conn)

	last_btc_trade = df5['price'].iloc[-1]
	last_btc_trade = float(last_btc_trade)
	print(last_btc_trade)

	positions = GetPositions()
	print(positions)
	
	if positions is None:	
		
		if ((signal_1m == 2) & (lstm_prediction > last_btc_trade)) or ((signal_3m == 2) & (lstm_prediction > last_btc_trade)): 
			
			order_functions.marketbuy('BTCUSD', .1, )
			stop_limit = last_btc_trade - atr
			profit_target = last_btc_trade + (atr * 2)

	else:
		

		qty = positions[0].qty

		if (signal_1m == 1) or (signal_3m == 1):
		
			MarketSell('BTCUSD', qty)		

		elif (last_btc_trade <= stop_limit) or (last_btc_trade >= profit_target):

			MarketSell('BTCUSD', qty)

	time.sleep(2)
