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
import time

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


def StopLimitProfitBuy(symbol, qty, limit_price, stop_price, take_profit):
    stop_limit_profit_order_data = StopLimitProfitOrderRequest(
	symbol=symbol, 
	side='buy', 
	type='stop_limit', 
	qty=qty,
	time_in_force='gtc', 
	limit_price=limit_price, 
	stop_price= stop_price,
	take_profit=dict(limit_price=take_profit)
    )

    trading_client.submit_order(stop_limit_profit_order_data)

def StopLimitProfitSell(symbol, qty, limit_price, stop_price, take_profit):
    stop_limit_profit_order_data = StopLimitProfitOrderRequest(
	symbol=symbol, 
	side='sell', 
	type='stop_limit', 
	qty=qty,
	time_in_force='gtc', 
	limit_price = limit_price, 
	stop_price= stop_price,
	take_profit=dict(limit_price=take_profit)
    )

    trading_client.submit_order(stop_limit_profit_order_data)


# Stop Limit Order: You have a price you want to buy and a stop, to prevent too much loss
def StopLimitBuy(symbol, qty, limit_price, stop_price):
    stop_limit_order_data = StopLimitOrderRequest(
	symbol=symbol, 
	side='buy', 
	type='stop_limit', 
	qty=qty,
	time_in_force='gtc', 
	limit_price=limit_price, 
	stop_price= stop_price
    )

    return trading_client.submit_order(stop_limit_order_data)

# Limit Order BUY: You just have a price you want to Buy at
def LimitBuy(symbol, qty, limit_price):
    limit_order_data = LimitOrderRequest(
	symbol=symbol,
	qty=qty,
	side=OrderSide.BUY,
	type='limit',
	time_in_force="gtc",
	limit_price=limit_price,
	)

    return trading_client.submit_order(limit_order_data)

# Limit Order SELL: You just have a price you want to Sell at
def LimitSell(symbol, qty, limit_price):
    limit_order_data = LimitOrderRequest(
	symbol=symbol,
	qty=qty,
	side=OrderSide.SELL,
	type='limit',
	time_in_force="gtc",
	limit_price=limit_price,
	)

    return trading_client.submit_order(limit_order_data)

# Market Order BUY: You are buying shares at the current price
def MarketBuy(symbol, qty):
    market_order_data = MarketOrderRequest(
	symbol=symbol,
	qty=qty,
	side=OrderSide.BUY,
	type='market',
	time_in_force="gtc",
	)

    return trading_client.submit_order(market_order_data)

# Market Order SELL: You are selling shares at the current price
def MarketSell(symbol, qty):
    market_order_data = MarketOrderRequest(
	symbol=symbol,
	qty=qty,
	side=OrderSide.SELL,
	type='market',
	time_in_force="gtc",
	)

    return trading_client.submit_order(market_order_data)
# Get all open positions and print each of them

def GetPositions():
	
    positions = trading_client.get_all_positions()
        
    for position in positions:
       	
       	for property_name, value in position:
            print(f"\"{property_name}\": {value}")

# Getting account information and printing it
# Shows currency type, available cash and buying power
def GetAccountInfo():
    account = trading_client.get_account()
    print('Currency:', account.cash)
    print('Available Cash:', account.cash)
    print('Buying Power:', account.buying_power)
 

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
	#	print(positions[0].qty)
	#MarketSell('BTCUSD', .09975)
	quit()
	if positions is None:	
		
		if ((signal_1m == 2) & (lstm_prediction > last_btc_trade)) or ((signal_3m == 2) & (lstm_prediction > last_btc_trade)): 
			
			MarketBuy('BTCUSD', .1)
			stop_limit = last_btc_trade - atr
			profit_target = last_btc_trade + (atr * 2)

	else:
		

		qty = positions[0].qty

		if (signal_1m == 1) or (signal_3m == 1):
		
			MarketSell('BTCUSD', qty)		

		elif (last_btc_trade <= stop_limit) or (last_btc_trade >= profit_target):

			MarketSell('BTCUSD', qty)

	time.sleep(2)
