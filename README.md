# Trading_Bot_9000

## Description 

This software is a crypto trading bot designed to work with Binance.US.  AS currently configured it runs on the Binance.US test API (?paper trading). The bot can play both the long and short side of the crypto market, but due to limitations on the Binance test API, only the long side is currently functional.  For full trading with this code, the actual Binance API is available to anyone with a funded Binance.US account. 


## Dependencies

MySQL (latest)
Python 3.8 or higher
Ubuntu Server 20.04 - Not required but as currently configured

Python Package Dependencies

Pandas
Numpy
Dotenv
Pandas TA
TALIB (comment lines X AND Y from make_binance_btc_ohlcv.py to skip this dependency)
Binance-Connector

## Installation

In order to install Tradingbot9000, you will need read/write credentials to a MySQL database, and root access to a Python 3.8 environment.  You will also needBinance API or Binance Test API keys.

The bot is broken down into 3 main areas of code.  

1)Data Acquistion - 

2)Signal Generation - 

3)Trading Code - 


## MVP User Stories

Our MVP will be based on the following user stories to start:

As an investor, I want to import historical cryptocurrency data 
- I expect the cruptocurrency data to have OHLCV data
- I expect to access cryptocurrency data as a pd.DataFrame

As an investor, I want to use an ML models to use for algorithmic trading.
- I expect to load the crypto data
- I expect to select a model
- I expect to train/fit the model
- I expect the model to predict what trades to make

As an investor, I want to make trades based on signals from my ML model
- I expect to use a Alpaca account configured for paper trading
- I expect to integrate the Alpaca SDK into my trading bot
- I expect that when I receive a buy signal, my trading bot will buy specified quantity of cryptocurrency
- I expect that when I receive a sell signal, my trading bot will sell specified quantity of cryptocurrency
- I expect to see my current orders in Alpaca portal
- I expect to see my current positions in Alpaca portal 

As an investor, I want my trading bot to run continuously at a specified interval 
- I expect that my trading bot will train continuously at a specified interval (eg every 10 secs)
- I expect that my trading bot will predict continuously at a specified interval (eg every 10 secs)
- I expect that my trading bot will detect a buy/sell signal and execute the trade


## Nice-to-Have User Stories
As an investor, I want to execute the trading bot for several ML models
- I expect to select different ML model 
- I expect to view results from trades in different Alpaca accounts
- I expect to determine which ML model was most successful 


## Implementation Tasks
- Historical Cryptocurrency Data
-- Dev: David
-- Reviewers: Quinn, Garrett, Derrick, Ryan, Kristen

- ML Model for Algorithmic Trading 
-- Dev: Garrett, Derrick, Ryan, Kristen
-- Reviewers: Quinn, David

- Alpaca Trading Client
-- Dev: Quinn, Kristen
-- Reviewers: Garrett, Derrick, Ryan, Kristen

- Automated Trading Bot Processes 
-- Dev: Quinn, David
-- Reviewers: Garrett, Derrick, Ryan, Kristen

## Technology Stack

This project uses:  
- Python 3.9.12 
- Pandas (1.4.2)
- Sci-kit Learn
- Keras
- TensorFlow
- hvPlot (0.7.3)
- Matplotlib(3.5.1)
- Pandas_ta (0.3.14b0)
- Amazon Web Services


## Installation

In order to use this application, you will need to install `Jupyter`, `pandas` and `hvPlot`. Below are the instructions for installing each required library.

- Installing Jupyter - To install Jupyter, please refer to the [Jupyter Installation Guide](https://jupyter.org/install).

- Installing pandas - To install `pandas`, please refer to the [pandas Installation Guide](https://pandas.pydata.org/pandas-docs/stable/getting_started/install.html).

- Installing hvPlot - To install `hvPlot`, please refer to the [hvPlot Installation Guide](https://pypi.org/project/hvplot).


## Usage

To launch the Notebook, perform the following steps:

1. Open Terminal.
2. Navigate to the location of the Notebook.
3. Enter `jupyter lab` at the Terminal prompt.
4. Verify that you can access Jupyter in your browser.
5. Once you have launched the notebook, you can then execute each section.

- Fetching Data
- Cleanup and Merging
- Displaying Historical Data
- MACD Analysis
- Monte Carlo Simulations

To use the web application, go to https://forte42-realestate-of-mind-streamlit-app-vov7jq.streamlitapp.com/

## Contributors

This sample application was authored by:

- Garrett Hernandez (gtkhhz@gmail.com)
- Quinn Wong (quinn.wong@gmail.com)
- Kristen Potter
- Derrick Decesares
- Ryan Mangum
- David Lampach


## License

The MIT License (MIT)

Copyright (c) 2022 Realestate of Mind

Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.

