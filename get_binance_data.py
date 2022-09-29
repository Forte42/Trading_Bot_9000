import pandas as pd
import sqlalchemy
import pymysql
from sqlalchemy import create_engine
from binance.spot import Spot
import time

engine = create_engine("mysql+pymysql://admin:52GxbFuetNqvFn@crypto-db.cb84pseap2n8.us-east-1.rds.amazonaws.com:3306/crypto",)

client = Spot()

while True:

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
	time.sleep(45)


