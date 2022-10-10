def trade_on_ema_signal():

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
	import click

	load_dotenv()

	host = os.getenv("HOST")
	dbname = os.getenv("DBNAME")
	username = os.getenv("USERNAME")
	password = os.getenv("PASSWORD")

	engine = create_engine(f"mysql+pymysql://{username}:{password}@{host}/{dbname}",)               
	conn = engine.connect()  
		


	click.clear()	
	df = {}
	df = pd.read_sql(f"SELECT ema_scalp_1m FROM signals order by tIMESTAMP desc LIMIT 1", conn) 
	signal_1m = df['ema_scalp_1m'].iloc[-1].astype(int)
	print(f'one minute signal --> {signal_1m}')
	df2 = {}
	df2 = pd.read_sql(f"SELECT ema_scalp_3m FROM signals ORDER BY Timestamp DESC LIMIT 1", conn)
	signal_3m = df2['ema_scalp_3m'].iloc[-1].astype(int)
	print(f'three minute signal --> {signal_3m}')
	df3 = {}
	df3 = pd.read_sql(f"SELECT timestamp, value FROM lstm_3m_signal ORDER BY timestamp DESC LIMIT 1", conn)
	lstm_prediction = df3['value'].iloc[-1].astype(float)
	print(f'lstm prediction --> {lstm_prediction}')
	df4 = {}
	df4 = make_binance_btc_ohlcv.return_dataframe('3m')
	atr = df4['ATR'].iloc[-1].astype(float)
	print(atr) 

	df5 = {}
	df5 = pd.read_sql('select * from binance_btc_0m order by id desc limit 1;', conn)

	last_btc_trade = df5['price'].iloc[-1]
	last_btc_trade = float(last_btc_trade)
	print(f' last btc trade --> {last_btc_trade}')
	
	if (((signal_1m == 2) & (lstm_prediction > last_btc_trade))) or (((signal_3m == 2) & (lstm_prediction > last_btc_trade))): 
			
		stop_limit = last_btc_trade - atr
		profit_target = last_btc_trade + (atr * 2)
		order_functions.bracket_market_buy('BTCUSDT', .1, stop_limit, profit_target, 'ema 1m_3m scalp')

	
