from binance.spot import Spot 
import pandas as pd
import time
from sqlalchemy import create_engine
import sqlalchemy
import pymysql

engine = create_engine("mysql+pymysql://admin:52GxbFuetNqvFn@crypto-db.cb84pseap2n8.us-east-1.rds.amazonaws.com:3306/crypto",)

client = Spot()

while True:

	ohlc_list = (client.klines("BTCUSDT", "1m", limit = 1000))

	df = {}
	df = pd.DataFrame(ohlc_list)
	df = df[:-1]
	
	df.rename(columns={0 : 'Timestamp', 1 : 'Open', 2 : 'High', 3 : 'Low', 4 : 'Close', 5 : 'Volume', 6 : 'Close_Timestamp' , 7 : 'QAV', 8 : 'Number_Of_Trades', 9 : 'TBB', 10 : 'TBQ' , 11 : 'NOT_APPLICABLE'}, inplace = True)
	
	try:
		last_timestamp = engine.execute("SELECT Timestamp FROM binance_btc_1m ORDER BY timestamp DESC LIMIT 1;")
		last_timestamp = last_timestamp.fetchone()
		last_timestamp = last_timestamp[0]
		print(last_timestamp)
	except:

		last_timestamp = 99999999999999999999

	
	print(df)
	
	if last_timestamp < 99999999999999999999:

		df = df[df['Timestamp'] > last_timestamp]
		df.to_sql(con=engine, name='binance_btc_1m', if_exists='append',chunksize=100, index=False)

	else:

		df.to_sql(con=engine, name='binance_btc_1m', if_exists='append',chunksize=100, index=False)

	print('success')
	time.sleep(45)
