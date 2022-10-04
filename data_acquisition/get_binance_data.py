def get_binance_btc_0m_data():


	import pandas as pd
	import sqlalchemy
	import pymysql
	from sqlalchemy import create_engine
	from binance.spot import Spot
	import time
	from dotenv import load_dotenv                                                                                                                                
	import os                                                                                                                                                     
																				      
																				      
	load_dotenv()                                                                                                                                                 
	host = os.getenv("HOST")                                                                                                                                      
	dbname = os.getenv("DBNAME")                                                                                                                                  
	username = os.getenv("USERNAME")                                                                                                                              
	password = os.getenv("PASSWORD")                                                                                                                              
																				      
	engine = create_engine(f"mysql+pymysql://{username}:{password}@{host}/{dbname}",)   

	client = Spot()

	
	trade_list = (client.trades("BTCUSDT", limit=1000))

	df = {}
	df = pd.DataFrame(trade_list)


	try:
		last_trade_id = engine.execute("SELECT id FROM binance_btc_trades ORDER BY id DESC LIMIT 1;")
		last_trade_id = last_trade_id.fetchone()
		last_trade_id = last_trade_id[0]
		print(last_trade_id)
	except:

		last_trade_id = 9999999999

	if last_trade_id < 9999999999:

		df = df[df['id'] > last_trade_id]
		df.to_sql(con=engine, name='binance_btc_trades', if_exists='append',chunksize=100, index=False)

	else:

		df.to_sql(con=engine, name='binance_btc_trades', if_exists='append',chunksize=100, index=False)

	print('success')


