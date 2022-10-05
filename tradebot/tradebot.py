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

df = pd.read_sql(f"SELECT ema_scalp_1m FROM signals order by tIMESTAMP desc LIMIT 1", conn) 
signal_1m = df['ema_scalp_1m'].iloc[-1].astype(int)
print(signal_1m)
df2 = pd.read_sql(f"SELECT ema_scalp_3m FROM signals ORDER BY Timestamp DESC LIMIT 1", conn)
signal_3m = df2['ema_scalp_3m'].iloc[-1].astype(int)
print(signal_3m)
df3 = pd.read_sql(f"SELECT timestamp, value FROM lstm_3m_signal ORDER BY timestamp DESC LIMIT 1", conn)
lstm_prediction = df3['value'].iloc[-1].astype(float)
print(lstm_prediction)

df4 = make_binance_btc_ohlcv.return_dataframe('3m')
atr = df4['ATR'].iloc[-1].astype(float)
print(atr) 

df5 = pd.read_sql('select * from binance_btc_trades order by id desc limit 1;', conn)

last_btc_trade = df5['price'].iloc[-1]
last_btc_trade = float(last_btc_trade)
print(last_btc_trade)

stop_price_buy = last_btc_trade - atr
take_profit_buy = last_btc_trade + (atr*2)
stop_price_sell = last_btc_trade + atr
take_profit_sell = last_btc_trade - (atr*2)

limit_buy_price = last_btc_trade + (last_btc_trade * .1)
limit_sell_price = last_btc_trade - (last_btc_trade * .1)


positions = GetPositions()
# First set the initial end_time for the orders
# Set to the current time so we fetch all orders up until now
# There's a limit to the number of orders received, but by selecting
# direction='desc' the API will fetch orders from this date BACKWARDS
end_time = datetime.datetime.now(datetime.timezone.utc).isoformat()

# Create an empty list to store our full order list
order_list = []

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

print(order_df[['filled_qty', 'filled_avg_price']])

#api.submit_order(
#    symbol='BTC/USD',
#    qty=.1,
#    side='buy',
#    type='market',
#    time_in_force='gtc',
#    order_class='simple')
#    #stop_loss={'stop_price': last_btc_trade * 0.95,
#    #           'limit_price':  last_btc_trade * 0.94},
#    #ta:e_profit={'limit_price': last_btc_trade * 1.05})

quit()  

if positions == 'None':
	
	if (signal_1m == 2) & (lstm_prediction > last_btc_trade): 

		StopLimitProfitBuy('BTC/USD', .1, limit_buy_price, stop_price_buy, take_profit_buy)

	if (signal_1m == 1) & (lstm_prediction < last_btc_trade):

		StopLimitProfitSell('BTC/USD', .1, limit_sell_price, stop_price_sell, take_profit_sell)

	else:

		pass


	

			

 
