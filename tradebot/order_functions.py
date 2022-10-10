def market_sell(symbol, qty):

	"""Function makes a clean market sell order for any binance symbol and returns the fill data"""

	import os
	from dotenv import load_dotenv
	from binance.spot import Spot 
	import pandas as pd
	from binance.lib.utils import config_logging
	from binance.error import ClientError

	# Load environmental variables

	load_dotenv()
	api_key = os.environ.get('binance_api')
	api_secret = os.environ.get('binance_secret')
	host = os.getenv("HOST")
	dbname = os.getenv("DBNAME")
	username = os.getenv("USERNAME")
	password = os.getenv("PASSWORD")

	# Initialize Binance Client

	client = Spot(key=api_key, secret=api_secret, base_url='https://testnet.binance.vision')

	# Market order sell function for Binance


	    
	params = {
	"symbol": symbol,
	"side": "SELL",
	"type": "MARKET",
	"quantity": qty
    }
    
	response = 0
	try:

		response = client.new_order(**params)
		print(response)
		return response

	except ClientError as error:
	
		print(
		"Found error. status: {}, error code: {}, error message: {}".format(
			error.status_code, error.error_code, error.error_message
		)
		)

	return response


def market_buy(symbol, qty):

	"""Function makes a clean market buy order for any binance symbol and returns the fill data"""

	import os
	from dotenv import load_dotenv
	from binance.spot import Spot 
	import pandas as pd
	from binance.lib.utils import config_logging
	from binance.error import ClientError

	# Load environmental variables

	load_dotenv()
	api_key = os.environ.get('binance_api')
	api_secret = os.environ.get('binance_secret')
	host = os.getenv("HOST")
	dbname = os.getenv("DBNAME")
	username = os.getenv("USERNAME")
	password = os.getenv("PASSWORD")

	# Initialize Binance Client

	client = Spot(key=api_key, secret=api_secret, base_url='https://testnet.binance.vision')

	# Market order sell function for Binance


	    
	params = {
	"symbol": symbol,
	"side": "BUY",
	"type": "MARKET",
	"quantity": qty
    }
    
	try:

		response = client.new_order(**params)
		print(response)
		return response

	except ClientError as error:
	
		print(
		"Found error. status: {}, error code: {}, error message: {}".format(
			error.status_code, error.error_code, error.error_message
		)
		)

	return response


def bracket_market_buy(symbol, qty, stop_loss, profit_target, strategy='none specified'):

	"""This function initiates a market buy order for BTCUSTD on binance and waits until stop loss and profit targets are reached to initiate sell order"""
	
	import json
	import os
	from dotenv import load_dotenv
	from binance.spot import Spot 
	import pandas as pd
	from sqlalchemy import create_engine
	from binance.lib.utils import config_logging
	from binance.error import ClientError
	import time
	from sqlalchemy.exc import SQLAlchemyError
	import click # Used for clearing output display
	import order_functions


	# Load environmental variables

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
	conn = engine.connect()

	order = order_functions.market_buy(symbol, qty)

	# Wait for order to be completely filled

	while not order['status'] == 'FILLED':

		time.sleep(.1)

	# Once order is filled use response data to calculate stop loss and profit target

	if order['status'] == 'FILLED':
		
		qty = float(order['executedQty'] )
		cost_basis = float(order['cummulativeQuoteQty']) / qty # Calculates the price of 1 BTC paid in trade
		buy_link = order['orderId']
		print(cost_basis)

			
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

		try:
			
			def get_last_btc_trade():
				
				""" This function gets last BTC price from binance_btc_0m table in MySQL """

				last_trade_id = engine.execute("SELECT id, price FROM binance_btc_0m ORDER BY id DESC LIMIT 1;")
				last_trade_id = last_trade_id.fetchone()
				last_trade_id = last_trade_id[1]
				last_trade_id = float(last_trade_id)
				print('Successfully acquired last bitcoin price from binance_btc_0m')
				print(last_trade_id)
				return last_trade_id

				last_trade_id = get_last_btc_trade()

		except SQLAlchemyError as e:
			
			error = str(e.__dict__['orig'])
			print(error)


		# Waits for either stop loss or profit target to be reached and then sells original order amt. 

		i=1
		while i == 1:
			
			click.clear() # This clears the output display
			last_trade_id = get_last_btc_trade()
			print(f'Waiting for Stop Loss - {stop_loss} or Profit Target {profit_target}')
			print(f'cost basis ---> {cost_basis}')	


			if last_trade_id > profit_target:
						
				order = order_functions.market_sell('BTCUSDT', qty)
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


				rs = conn.execute(f'INSERT INTO sell_orders (Order_id, Symbol, Transact_Time, Price, Ordered_Qty, Executed_Qty, Cost_Basis, Status, Time_In_Force, Order_Type, Order_Side, Linked_Order, Strategy) VALUES ({order_id},"{symbol}", {transact_time}, {price}, {ordered_qty}, {executed_qty}, {cost_basis},"{status}","{time_in_force}", "{order_type}", "{order_side}",{buy_link}, "{strategy}")')
				rs = conn.execute(f'UPDATE buy_orders SET Linked_Order = {order_id} WHERE Order_id = "{order_id}";') 
			i=0
			
			if last_trade_id < stop_loss:
				
				order = order_functions.market_sell('BTCUSDT', qty)
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


				rs = conn.execute(f'INSERT INTO sell_orders (Order_id, Symbol, Transact_Time, Price, Ordered_Qty, Executed_Qty, Cost_Basis, Status, Time_In_Force, Order_Type, Order_Side, Linked_Order, Strategy) VALUES ({order_id},"{symbol}", {transact_time}, {price}, {ordered_qty}, {executed_qty}, {cost_basis},"{status}","{time_in_force}", "{order_type}", "{order_side}",{buy_link}, "{strategy}")')
				rs = conn.execute(f'UPDATE buy_orders SET Linked_Order = {order_id} WHERE Order_id = "{buy_link}";') 
				i=0

