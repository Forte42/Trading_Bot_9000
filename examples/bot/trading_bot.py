import pandas as pd
import numpy as np
from dotenv import load_dotenv
import os
import requests
import random
import alpaca_trade_api as tradeapi
import datetime
from alpaca.trading.client import TradingClient
from alpaca.trading.requests import MarketOrderRequest
from alpaca.trading.enums import OrderSide, TimeInForce
from apscheduler.schedulers.blocking import BlockingScheduler

# Load environment variables
load_dotenv()

# Set api_key and secret_key
alpaca_api_key = os.getenv("ALPACA_API_KEY")
alpaca_secret_key = os.getenv("ALPACA_SECRET_KEY")

# Create TradingClient
trading_client = TradingClient(alpaca_api_key, alpaca_secret_key, paper=True)

def bot_job():
    print("Executing bot job...")
    # Instantiate model
    # TODO: Instantiate the model here...
    
    # Train model 
    # TODO: Train the model or load a saved model here
    
    # Generate predictions
    # TODO: Generate the predictions.   For now, we're just 
    # going to randomly generate a buy or sell signal. 
    pred = bool(random.getrandbits(1))
    # print(f"-- signal: {pred}")
    print(pred)
    
    # Execute order
    # Sell
    if pred == 0:
        print("Executing sell order...")
        market_order_data = MarketOrderRequest(
                            symbol="ETH/USD",
                            qty=0.25,
                            side=OrderSide.SELL,
                            time_in_force="gtc"
                            )


        # Market order
        market_order = trading_client.submit_order( market_order_data)
        market_order
        
        
        
    elif pred == 1:
        print("Executing buy order...")
        market_order_data = MarketOrderRequest(
                            symbol="ETH/USD",
                            qty=0.25,
                            side=OrderSide.BUY,
                            time_in_force="gtc"
                            )

        # Market order
        market_order = trading_client.submit_order( market_order_data)
        market_order


print("Creating scheduler...")
scheduler = BlockingScheduler(job_defaults={'misfire_grace_time': 15*60})

print("Adding scheduler job...")
#scheduler.add_job(bot_job, 'cron', day_of_week='mon-fri', minute=1, jitter=120, timezone='America/New_York')
scheduler.add_job(bot_job, 'interval', minutes=1)

print("Starting scheduler...")
scheduler.start()