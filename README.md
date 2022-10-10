# Trading_Bot_9000

## Problem Statement

Trading cryptocurrencies can potentially be an extremely lucrative means of investment. It is a fairly new, disruptive investment vehicle and there are promises of great rewards.

However, with anything that is high reward, there are also great risks and several challenges due to the nature of cryptocurrency. One such challenge is that cryptocurrencies are traded around the clock globally and a signal human trader cannot stay awake all day trading. This results in missed buying and selling opportunities, as there may be events that affect the prices of certain assets or the entire market on the whole. Humans cannot detect every signal that points to a buying or selling opportunity. Finally, with any investing, human emotions comes into play. Since crypocurrencies are especially volatile, this can potentially result in erratic and impulsive decisions.

Algorithimic trading and automated bots can eliminate some risks as well as overcoming challenges associated with trading cryptocurrencies. Machine Learning allows us to train models that can predict buying and selling opportunities. Automated trading bots can also trade 24 hours a day, 7 days a week. Finally, bots do not have emotions, so this eliminates any problems caused by human emotions.

---

## Solution Overview

For our project, we are implementing an automated bot that incorporates algorithmic trading to buy and sell cryptocurrencies. The automated bot has several features:

- Data Retrieval
- Transformation and Modeling
- Trading

![alt text](/images/flowchart.png)

### 1. Data Retrieval

Data is retrieved through Binance, one the largest cryptocurrency exchanges in the world. The data retrieval occurs through Binance's REST APIs and is stored into a MySQL database for additional processing. Data is retrieved at regular intervals throughout the day.

### 2. Transformation and Modeling

**2.1. Long Short Term Memory (LSTM)**

We are incorporating LSTM, a type of artificial neural network, to allow us to incorporate machine learning into our trading bot.

**2.2. Bitcoin Fear-and-Greed Index**

One of the features that will be used for the LSTM model is the Bitcoin Fear-and-Greed index, which is an index that takes into account the following factors:

- Volatility
- Market Volume
- Social Media
- Dominance
- Trends

**2.3. Scalping Trading Strategies**  
For our scalping model we use three EMAs (exponential moving averages) to determine whether our asset is in an uptrend or a downtrend. We then moniter the open and close of our fifteen-minute candles to determine once it crosses the shortest EMA. If it crosses back over the EMA in the next candle then we will initiate our trade. We utilize a strict exit strategy so can minimize our losses. Setting our take profit limit to double our stop loss allows the strategy to be profitable even when winning less than 50% of the trades.

We also have a scalping model that uses an EMA as well VWAP to determine trend. It then follows a similar strategy outlined above.

### 3. Trading

The trading bot executes a trading task that reads the MySQL database for buy and sell signals. The trading task will analyze the latest buy and sell signals and determine whether to execute a trade.

---

## Technology Stack

This example uses the following technologies:

### MySQL

MySQL is used to store the following:

- Historical Bitcoin Trades
- Buy and Sell Signals

### Machine Learning Technologies

- **Scikit-Learn** - Scikit-Learn is an open-source machine learning library for the Python programming language. Please see [Scikit-Learn documentation](https://www.tutorialspoint.com/scikit_learn/scikit_learn_introduction.htm) for more information.
- **TensorFlow** - End-to-end open-source platform for machine learning
- **Keras** - Abstraction layer on top of TensorFlow that makes it easier to build models

### Python Technologies

- **Jupyter** - Jupyter is a web-based interactive development environment for data science and analysis. Please see [Jupyter documentation](https://jupyter.org/) for more information.
- **pandas** - pandas is a software library written for the Python programming language for data manipulation and analysis. Please see [pandas documentation](https://pandas.pydata.org/) for more information.
- **numpy**
- **pandas_ta**

---

## Installation

The project's dependencies are stored in `requirements.txt`. To install these dependencies, you can execute the following command:

`pip install -r requirements.txt`

Here is a list of the dependencies:
All of the dependencies are listed below:

```
# reg_model.ipynb and up_or_down_model.ipynb requirements
matplotlib==3.5.1
numpy==1.21.5
pandas==1.3.5
python-dotenv==0.21.0
requests==2.27.1
scikit_learn==1.1.2
tensorflow==2.10.0

# non-machine-learning-strategies requirements
Backtesting==0.3.3
pandas_ta==0.3.14b0
plotly==5.6.0
yfinance==0.1.77
```

---

## Usage

### Running the Code

To run the code, perform the following steps:

1. Download all files
2. Use the files in the main folder:
  - get_data.py: scheduler for retrieving data
  - get_signals.py: scheduler for retrieving signal information
  - reg_model.ipynb: Regression LSTM model with yahoo finance data jupyter file
  - run_signal.sh: script used to start the signal generator
  - tradebot.py: EMA trading signal scheduler
3. Use the py files in the tradebot folder:
  - b.py: creates sqlalchemy MySQL Connection, puts in an order and waits for order to be filled before adding on a stop and a limit.
  - ema_trade_bot.py: trades off of ema signals
  - get_binance_balances.py: Queries Binance API for account balances and write them to MySQL table 'binance_account_balances'
  - make_binance_btc_ohlcv.py: Functions to return a DataFrame from binance
  - order_functions.py: Functions to generate trade orders from binance
  - track_order.py: Imports
  - trade_fear_greed.py: If statements that will execute trades based on Fear and Green Index machine learning
4. Use the py files in the signal_generation folder:
  - btc_ema_scalp_0m.py: EMA signal generation for BTC trade data
  - ema_1m_3m_scalp.py: EMA signal generation for BTC on a 1m and 3m timeframe
  - fear_greed_signal.py: Fear and Greed machine learning model
  - make_binance_btc_ohlcv.py: making binance btc data into ohlcv
5. Use the py files in the models folder:
  - make_lstm_prediction.py: Function that trains and makes a prediction given a DataFrame
  - my_model.h5: Output of make_lstm_prediction.py file
  - build_lstm_model.py: LSTM model prediction code
  - model_storage Folder: Stores models
6. The files in the images folder: show flow chart of proccesses
7. Use the py files in the data_transformation folder:
  - btc_volume_analysis.py: analysis volume from binance BTC data
  - make_binance_btc_ohlcv.py: Function that turns BTC binance data into OHLCV
8. Use the py files in the data_explorations folder:
  - In the examples/binance Folder:
    - binance_client.py: Functions that generate buy and sell orders from binance
  - In the non-machine-learning-strategies Folder:
    - BTCUSD_Candlestick_15_M_ASK_05.08.2019-29.04.2022.csv: Candlestick data from 05.08.2019-29.04.2022
    - EMA_Scalping_BTC.ipynb: EMA scalping strategy in jupyter file 
    - VWAP_BTC.ipynb: VWAP strategy in jupyter file
  - reg_model.ipynb: Regression LSTM model with yahoo finance data
  - up_or_down_model.ipynb: Regression LSTM model with yahoo finance data and Fear and Greed Index
9. Use the py files in the data_acquisition folder:
  - fear_greed.py: Import fear and greed data
  - get_binance_btc_0m.py: Import binance trade data
  - get_binance_btc_1d.py: Import binance 1 day data
  - get_binance_btc_1m.py: Import binance 1 minute data
  - get_binance_btc_30m.py: Import binance 30 minute data
  - get_binance_btc_3m.py: Import binance 3 minute data
  - get_binance_ohlcv_bar.py: Import binance ohlcv bar data
  
---

## Contributors

This application was authored by:

- David Lampach
- Derick DeCesare (derick.decesare@gmai.com)
- Garrett Hernandez (gtkhhz@gmail.com)
- Kristen Potter
- Quinn Wong (quinn.wong@gmail.com)
- Ryan Mangum

---

## License

The MIT License (MIT)

Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
