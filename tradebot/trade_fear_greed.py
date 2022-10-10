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

df = pd.read_sql(f'SELECT * FROM fear_greed ORDER BY timestamp DESC LIMIT 1;',conn)

entry_exit = df['Entry_Exit'].iloc[-1]
coins_to_transact = df['Number_Coins_To_Transact'].iloc[-1]
coins_to_transact = (float(coins_to_transact))/10
strategy = 'fear greed signal'
coins_to_transact =3.4 
entry_exit = -1
print(entry_exit)
print(coins_to_transact)

if coins_to_transact > 0:

	if entry_exit > 0:
		
		order = order_functions.market_buy('BTCUSDT', coins_to_transact)
		order_id = order['orderId']
		symbol = order['symbol']
		transact_time = order['transactTime']
		price = order['price']
		ordered_qty = order['origQty']
		executed_qty = order['executedQty']
		cost_basis = order['cummulativeQuoteQty']
		status = order['status']
		time_in_force = order['timeInForce']
		order_type = order['type']
		order_side = order['side']
		rs = conn.execute(f'INSERT INTO buy_orders (Order_id, Symbol, Transact_Time, Price, Ordered_Qty, Executed_Qty, Cost_Basis, Status, Time_In_Force, Order_Type, Order_Side, Strategy) VALUES ({order_id},"{symbol}", {transact_time}, {price}, {ordered_qty}, {executed_qty}, {cost_basis},"{status}","{time_in_force}", "{order_type}", "{order_side}", "{strategy}")')
 
	if entry_exit < 0:
		
		order = order_functions.market_sell('BTCUSDT', coins_to_transact)
		order_id = order['orderId']
		symbol = order['symbol']
		transact_time = order['transactTime']
		price = order['price']
		ordered_qty = order['origQty']
		executed_qty = order['executedQty']
		cost_basis = order['cummulativeQuoteQty']
		status = order['status']
		time_in_force = order['timeInForce']
		order_type = order['type']
		order_side = order['side']
		rs = conn.execute(f'INSERT INTO sell_orders (Order_id, Symbol, Transact_Time, Price, Ordered_Qty, Executed_Qty, Cost_Basis, Status, Time_In_Force, Order_Type, Order_Side, Strategy) VALUES ({order_id},"{symbol}", {transact_time}, {price}, {ordered_qty}, {executed_qty}, {cost_basis},"{status}","{time_in_force}", "{order_type}", "{order_side}", "{strategy}")')

