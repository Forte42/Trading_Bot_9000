import logging
from binance.spot import Spot as Client
from binance.lib.utils import config_logging
from binance.error import ClientError
from dotenv import load_dotenv
import os

# This is sample Python client that wraps Binance's new_order API to simplify 
# the following trade types: 
# 
# - Buy Limit
# - Sell Limit
# - Buy Market
# - Sell Market
#
# In order to use the client, you will need to create a test account on 
# Binance's platform:   https://testnet.binance.vision/
#
# You will then need to generate a api key and a secret key and place this in 
# a .env file.   The directions for generating the keys are in the link above.
#
# REST APIs - Binance REST API docs can be found here:  
#    https://binance-docs.github.io/apidocs/spot/en/#change-log
#
# If you want to play around with the REST APIs, you can use POSTMan, which is an 
# application designed specifically for testing REST APIs.  Binance has put together
# plenty of REST API examples for POSTMan here:  
#    https://github.com/binance/binance-api-postman
# 
# Python SDK - The binance client uses the following Python connector: 
#    https://github.com/binance/binance-connector-python
# 

# Stop Limit Order Take Profit: You have a price you want to buy,a stop and a take profit price, 
# to prevent too much loss and capture your gains
def StopLimitProfitBuy(symbol, qty, limit_price, stop_price, take_profit):
    # params = {
    #     "symbol": symbol,
    #     "side": "SELL",
    #     "type": "LIMIT",
    #     "timeInForce": "GTC",
    #     "quantity": qty,
    #     "price": 9500,
    # }
    # try:
    #     response = client.new_order(**params)
    #     logging.info(response)
    #     return response
    # except ClientError as error:
    #     logging.error(
    #         "Found error. status: {}, error code: {}, error message: {}".format(
    #             error.status_code, error.error_code, error.error_message
    #         )
    #     )
    return

def StopLimitProfitSell(symbol, qty, limit_price, stop_price, take_profit):
    # return trading_client.submit_order(stop_limit_profit_order_data)
    # params = {
    #     "symbol": symbol,
    #     "side": "BUY",
    #     "type": "STOP_LOSS",
    #     "timeInForce": "GTC",
    #     "quantity": qty,
    #     "stopPrice": stop_price,
    # }
    # try:
    #     response = client.new_order(**params)
    #     logging.info(response)
    #     return response
    # except ClientError as error:
    #     logging.error(
    #         "Found error. status: {}, error code: {}, error message: {}".format(
    #             error.status_code, error.error_code, error.error_message
    #         )
    #     )
    return

# Stop Limit Order: You have a price you want to buy and a stop, to prevent too much loss
def StopLimitBuy(symbol, qty, stop_price):
    # return trading_client.submit_order(stop_limit_order_data)
    params = {
        "symbol": symbol,
        "side": "BUY",
        "type": "STOP_LOSS",
        "quantity": qty,
        "stopPrice": stop_price,
    }
    try:
        response = client.new_order(**params)
        logging.info(response)
        return response
    except ClientError as error:
        logging.error(
            "Found error. status: {}, error code: {}, error message: {}".format(
                error.status_code, error.error_code, error.error_message
            )
        )

# Limit Order BUY: You just have a price you want to Buy at
def LimitBuy(symbol, qty, limit_price):
    params = {
        "symbol": symbol,
        "side": "BUY",
        "type": "LIMIT",
        "timeInForce": "GTC",
        "quantity": qty,
        "price": limit_price,
    }
    try:
        response = client.new_order(**params)
        logging.info(response)
        return response
    except ClientError as error:
        logging.error(
            "Found error. status: {}, error code: {}, error message: {}".format(
                error.status_code, error.error_code, error.error_message
            )
        )

# Limit Order SELL: You just have a price you want to Sell at
def LimitSell(symbol, qty, limit_price):
    params = {
        "symbol": symbol,
        "side": "SELL",
        "type": "LIMIT",
        "timeInForce": "GTC",
        "quantity": qty,
        "price": limit_price,
    }
    try:
        response = client.new_order(**params)
        logging.info(response)
        return response
    except ClientError as error:
        logging.error(
            "Found error. status: {}, error code: {}, error message: {}".format(
                error.status_code, error.error_code, error.error_message
            )
        )

# Market Order BUY: You are buying shares at the current price
def MarketBuy(symbol, qty):
    params = {
        "symbol": symbol,
        "side": "BUY",
        "type": "MARKET",
        "quantity": qty
    }
    try:
        response = client.new_order(**params)
        logging.info(response)
        return response
    except ClientError as error:
        logging.error(
            "Found error. status: {}, error code: {}, error message: {}".format(
                error.status_code, error.error_code, error.error_message
            )
        )


# Market Order SELL: You are selling shares at the current price
def MarketSell(symbol, qty):
    params = {
        "symbol": symbol,
        "side": "SELL",
        "type": "MARKET",
        "quantity": qty
    }
    try:
        response = client.new_order(**params)
        logging.info(response)
        return response
    except ClientError as error:
        logging.error(
            "Found error. status: {}, error code: {}, error message: {}".format(
                error.status_code, error.error_code, error.error_message
            )
        )



# Init logging
config_logging(logging, logging.DEBUG)

# Loading environment variables
logging.info("Loading environment variables...")
load_dotenv()

# Set api_key and secret_key
logging.info("Setting Binance api_key and secret_key...")
key = os.getenv("BINANCE_API_KEY")
secret = os.getenv("BINANCE_SECRET_KEY")
logging.info("Binance api_key and secret_key are loaded.")

# Create Binance client
logging.info("Creating binance client...")
client = Client(key, secret, base_url="https://testnet.binance.vision")

# Get server timestamp
logging.info(client.time())

# Get account and balance information
logging.info(client.account())

# Example - Limit buy
LimitBuy("BTCUSDT", 0.1, 18000)

# Example - Limit sell
LimitSell("BTCUSDT", 0.1, 22000)

# Example - Market buy
MarketBuy("BTCUSDT", 0.1)

# Example - Market sell
MarketSell("BTCUSDT", 0.1)

# Example - Stop limit buy
# StopLimitBuy("BTCUSDT", 0.1, 19000)



