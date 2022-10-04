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
from sqlalchemy import create_engine
import pymysql
import sqlalchemy


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

# symbol='ETH/USD'
# qty = 1
# side='buy'
# limit_price= 1000.00
# stop_price=999.90
# take_profit= 2000.00

# Stop Limit Order Take Profit: You have a price you want to buy,a stop and a take profit price, 
# to prevent too much loss and capture your gains
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
 

# Helpful Site to Explain Order Types: https://alpaca.markets/docs/api-references/trading-api/orders/

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
engine = create_engine(f"mysql+pymysql://{username}:{password}@{host}/{dbname}",)               
conn = engine.connect()  

df = pd.read_sql(f"SELECT ema_scalp_1m FROM signals LIMIT 1", conn) 
signal = df['ema_scalp_1m'].iloc[-1]
print(signal)

while true:
	


	if signal = 2:

		MarketBuy('BTC/USD', .1)

	if signal = 1:

		MarketSell('BTC/USD', .1)

	else:

		pass

			

 
