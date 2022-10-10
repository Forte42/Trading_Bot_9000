def get_binance_btc_0m_data():

	""" Gets trade by trade data from Binance and writes it to 'binance_btc_0m' table in MySQL crypto DB """


	import pandas as pd
	import sqlalchemy
	import pymysql
	from sqlalchemy import create_engine
	from binance.spot import Spot
	import time
	from dotenv import load_dotenv                                                                                                       
	import os
	      
	# Load environmental variables from dotenv file																				      
	load_dotenv()
	host = os.getenv("HOST")
	dbname = os.getenv("DBNAME")
	username = os.getenv("USERNAME")
	password = os.getenv("PASSWORD")                                                                                                                              
	# Create sqlalchemy MySQL Connection																				      
	engine = create_engine(f"mysql+pymysql://{username}:{password}@{host}/{dbname}",)   

	# Create Binance API Connection

	client = Spot()

	# Get list of last 1000 trades in BTCUSDT from Binance
	
	trade_list = (client.trades("BTCUSDT", limit=1000))

	# Initialize dataframes for data handling

	df = {}
	df = pd.DataFrame(trade_list)

	# Attempt MySQL query to get last timestamp from binance_btc_trades table

	try:
		last_trade_id = engine.execute("SELECT id FROM binance_btc_0m ORDER BY id DESC LIMIT 1;")
		last_trade_id = last_trade_id.fetchone()
		last_trade_id = last_trade_id[0]
		print('Successfully acquired last timestamp from binance_btc_0m')
		print(last_trade_id)
	
	except SQLAlchemyError as e:
  		
		error = str(e.__dict__['orig'])
		last_trade_id = 9999999999
		return error

	print(df)

	# Write latest trades to binance_btc_0m table

	if last_trade_id < 9999999999:

		df = df[df['id'] > last_trade_id]
		df.to_sql(con=engine, name='binance_btc_0m', if_exists='append',chunksize=100, index=False)

	else:

		df.to_sql(con=engine, name='binance_btc_0m', if_exists='append',chunksize=100, index=False)

	print('success')
	
