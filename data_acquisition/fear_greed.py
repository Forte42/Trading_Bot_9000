def get_fear_greed_daily_data():
	
	""" Gets the daily fear and greed indexdata and writes it to 'fear_greed' table in MySQL crypto DB """
	
	""" data url -->  https://api.alternative.me/fng/?limit=0  """
	
	import time
	import pandas as pd
	import numpy as np
	import json
	import hvplot.pandas
	import requests
	import yfinance as yf
	import datetime
	import sqlalchemy
	import pymysql
	import os
	from dotenv import load_dotenv
	from sqlalchemy import create_engine

	load_dotenv()

	host = os.getenv("HOST")
	dbname = os.getenv("DBNAME")
	username = os.getenv("USERNAME")
	password = os.getenv("PASSWORD")

	engine = create_engine(f"mysql+pymysql://{username}:{password}@{host}/{dbname}",)
	conn = engine.connect


	# use GET method and connect to API endpoint (Fear and Greed Index API)
	r = requests.get('https://api.alternative.me/fng/?limit=0')

	df = pd.DataFrame(r.json()['data'])
	print(df)

	# convert the value to an integer instead of an object
	df['value'] = df.value.astype(int)

	# convert timestamp to usable format
	df['timestamp_temp'] = (df['timestamp']).astype(int)
	df['timestamp'] = pd.to_datetime(df['timestamp'], unit='s')

	# set index to timsetamp

	df = df.set_index('timestamp')

	# reorganize data to oldest data points first
	df = df[::-1]

	btc_df = yf.download('BTC-USD')[['Close']]
	btc_df.index.name = 'timestamp'

	data_df = df.merge(btc_df, on ='timestamp')

	# drop time_until_update column
	data_df = data_df.drop(columns='time_until_update')

	# add percent change column and drop the null value from the shift
	data_df['pct_change'] = data_df['Close'].pct_change()

	# drop the null value
	data_df = data_df.dropna()

	data_df['Change'] = data_df['value_classification'].ne(data_df['value_classification'].shift().bfill()).astype(int)

	# convert the value_classifications to integers for use in machine learning models

	classification_int = []
	for string in data_df['value_classification']:

		if string == 'Extreme Fear':
			classification_int.append(int(0))

		elif string == 'Fear':
			classification_int.append(int(1))

		elif string == 'Neutral':
			classification_int.append(int(2))

		elif string == 'Greed':
			classification_int.append(int(3))

		elif string == 'Extreme Greed':
			classification_int.append(int(4))

	data_df['classification_int'] = classification_int	

	# Attempt MySQL query to get last timestamp from fear_greed table

	try:
		last_timestamp = engine.execute("SELECT timestamp_temp FROM fear_greed ORDER BY timestamp_temp DESC LIMIT 1;")                                                 
		last_timestamp = last_timestamp.fetchone()
		print(last_timestamp)
		last_timestamp = int(last_timestamp[0])
		print(last_timestamp) 

	except SQLAlchemyError as e:
	
		error = str(e.__dict__['orig'])
		last_timestamp = 9999999999
		print(last_timestamp)
		return error

	if last_timestamp != 9999999999:

		data_df = data_df.dropna()
		data_df=data_df[data_df['timestamp_temp'] > last_timestamp]
		data_df.to_sql(con=engine, name='fear_greed', if_exists='append',chunksize=100, index=True)

	else:


		data_df.to_sql(con=engine, name='fear_greed', if_exists='append',chunksize=100, index=True)

	time.sleep(120)