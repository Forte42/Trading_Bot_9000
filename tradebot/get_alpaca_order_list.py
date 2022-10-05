def get_orders_from_alpaca():

	import time
	import pandas as pd
	import numpy as np
	from dotenv import load_dotenv
	import os
	import requests
	import alpaca_trade_api as tradeapi
	import datetime
	from alpaca.trading.client import TradingClient
	from alpaca.trading.requests import MarketOrderRequest
	from alpaca.trading.enums import OrderSide, TimeInForce
	from alpaca.trading.requests import LimitOrderRequest
	from alpaca.trading.requests import StopLimitOrderRequest
	#from alpaca.trading.requests import StopLimitProfitOrderRequest

	from sqlalchemy import create_engine
	import pymysql
	import sqlalchemy
	import make_binance_btc_ohlcv

	# Load the environment variables and Set API
	load_dotenv()

	alpaca_api_key = "PKNZWF061XNUQBFZ2QZ0"
	alpaca_secret_key = "x9ehkKaBeseh6omqpl4X9GsCF4nTqHzqLyvIvTar"


	trading_client = TradingClient(alpaca_api_key, alpaca_secret_key, paper=True)

	base_url = 'https://paper-api.alpaca.markets'

	api = tradeapi.REST(
	    key_id=alpaca_api_key,
	    secret_key=alpaca_secret_key,
	    base_url=base_url,
	    api_version='v2'
	)

	host = os.getenv("HOST")
	dbname = os.getenv("DBNAME")
	username = os.getenv("USERNAME")
	password = os.getenv("PASSWORD")

	# Set Connection to MySQL DB

	engine = create_engine(f"mysql+pymysql://{username}:{password}@{host}/{dbname}",)

	conn = engine.connect()

	end_time = datetime.datetime.now(datetime.timezone.utc).isoformat()

	# Create an empty list to store our full order list
	order_list = []
	order_df= {}

	# Set the 'chunk size' to the 500 max
	CHUNK_SIZE = 500

	while True:
	  # Get the max chunk
	  order_chunk = api.list_orders(status='all', 
					nested='False', 
					direction='desc', 
					until=end_time,
					limit=CHUNK_SIZE)
	  
	  if order_chunk:
	    # Have orders so add to list
	    order_list.extend(order_chunk)
	    # Set end_time for next chunk to earliest fetched order
	    end_time = order_chunk[-1].submitted_at.isoformat()

	  else:
	    # No more orders. Make a dataframe of entire list of orders
	    # Then exit
	    order_df = pd.DataFrame([order._raw for order in order_list])
	    break

	order_df['qty'] = order_df['qty'].astype(float)
	order_df['limit_price'] = order_df['limit_price'].astype(float)
	order_df['stop_price'] = order_df['stop_price'].astype(float)
	order_df['filled_qty'] = order_df['filled_qty'].astype(float)
	order_df['id'] = order_df['id'].astype(str)
	order_df['filled_avg_price'] = order_df['filled_avg_price'].astype(float)
	order_df['created_at'] = pd.to_datetime(order_df['created_at'])
	order_df['updated_at'] = pd.to_datetime(order_df['updated_at'])
	order_df['submitted_at'] = pd.to_datetime(order_df['submitted_at'])
	order_df['filled_at'] = pd.to_datetime(order_df['filled_at'])
	order_df['expired_at'] = pd.to_datetime(order_df['expired_at'])
	order_df['canceled_at'] = pd.to_datetime(order_df['canceled_at'])
	order_df['failed_at'] = pd.to_datetime(order_df['failed_at'])
	order_df['replaced_at'] = pd.to_datetime(order_df['expired_at'])


	id_df = pd.read_sql('SELECT id FROM alpaca_order_list', conn)
	print(len(id_df))
	duplicates = set(order_df.id).intersection(id_df.id)

	print(duplicates)
	print(len(duplicates))
	for duplicate in duplicates:

		order_df = order_df[order_df.id != duplicate] 

	print(order_df)

	def pause():
		programPause = input("Press the <ENTER> key to continue...")

	order_df.to_sql('alpaca_order_list', con=engine, if_exists='append')

		

				

	 
