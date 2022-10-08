def update_binance_account_balances():

	import json
	import os
	from dotenv import load_dotenv
	from binance.spot import Spot 
	import pandas as pd
	from sqlalchemy import create_engine


	load_dotenv()
	api_key = os.environ.get('binance_api')
	api_secret = os.environ.get('binance_secret')
	host = os.getenv("HOST")
	dbname = os.getenv("DBNAME")
	username = os.getenv("USERNAME")
	password = os.getenv("PASSWORD")
	
	# Initialize Binance Client

	client = Spot(key=api_key, secret=api_secret, base_url='https://testnet.binance.vision')

	# Create sqlalchemy MySQL Connection                                                                                                                                                                  
	engine = create_engine(f"mysql+pymysql://{username}:{password}@{host}/{dbname}",)

	# Query Binance API for account balances and write them to MySQL table 'binance_account_balances'

	account_dump = json.dumps(client.account())
	balances = json.loads(account_dump)
	balances = (balances['balances'])
	df = pd.DataFrame(balances)
	df.to_sql(con=engine, name='binance_account_balances', if_exists='replace',chunksize=100, index=False)

