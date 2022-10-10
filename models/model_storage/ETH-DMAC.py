#!/usr/bin/env python
# coding: utf-8

# In[1]:


import pandas as pd
import numpy as np
from pathlib import Path
from dotenv import load_dotenv
import hvplot.pandas
import os
import requests
import datetime
from alpaca.data.historical import CryptoHistoricalDataClient
from alpaca.data.requests import CryptoBarsRequest
from alpaca.data.requests import CryptoLatestQuoteRequest
from alpaca.data.requests import CryptoTradesRequest
from alpaca.data.timeframe import TimeFrame


# In[2]:


load_dotenv()


# In[3]:


alpaca_api_key = os.getenv("ALPACA_API_KEY")
alpaca_secret_key = os.getenv("ALPACA_SECRET_KEY")


# In[4]:


type(alpaca_api_key)


# In[5]:


crypto_client = CryptoHistoricalDataClient(alpaca_api_key, alpaca_secret_key)


# In[6]:


request_params = CryptoBarsRequest(
    symbol_or_symbols=["ETH/USD"],
    timeframe=TimeFrame.Day,
    start="2012-01-01 00:00:00"
)

eth_bars = crypto_client.get_crypto_bars(request_params)

eth_df = eth_bars.df


# In[7]:


eth_df = eth_df.reset_index()


# In[8]:


eth_df = eth_df.set_index('timestamp')


# In[9]:


eth_df['close'].hvplot()


# In[10]:


# Filter the date index and close columns
signals_df = eth_df[['close']]

# Set the short window and long windows
short_window = 1
long_window = 30

# Generate the short and long moving averages (50 and 100 days, respectively)
signals_df['EMA_Short'] = signals_df['close'].ewm(span=short_window).mean()
signals_df['EMA_Long'] = signals_df['close'].ewm(span=long_window).mean()
signals_df['Signal'] = 0.0

# Generate the trading signal 0 or 1,
# where 1 is the short-window (EMA1) greater than the long-window (EMA30)
# and 0 is when the condition is not met
signals_df['Signal'][short_window:] = np.where(
    signals_df['EMA_Short'][short_window:] > signals_df['EMA_Long'][short_window:], 1.0, 0.0
)

# Calculate the points in time when the Signal value changes
# Identify trade entry (1) and exit (-1) points
signals_df['Entry/Exit'] = signals_df['Signal'].diff()


# In[11]:


# view the dataframe
signals_df.head(50)


# In[12]:


# Visualize exit position relative to close price
exit = signals_df[signals_df['Entry/Exit'] == -1.0]['close'].hvplot.scatter(
    color='yellow',
    marker='v',
    size=200,
    legend=False,
    ylabel='Price in $',
    width=1000,
    height=400
)

# Visualize entry position relative to close price
entry = signals_df[signals_df['Entry/Exit'] == 1.0]['close'].hvplot.scatter(
    color='purple',
    marker='^',
    size=200,
    legend=False,
    ylabel='Price in $',
    width=1000,
    height=400
)

# Visualize close price for the investment
security_close = signals_df[['close']].hvplot(
    line_color='lightgray',
    ylabel='Price in $',
    width=1000,
    height=400
)

# Visualize moving averages
moving_avgs = signals_df[['EMA_Short', 'EMA_Long']].hvplot(
    ylabel='Price in $',
    width=1000,
    height=400
)

# Create the overlay plot
entry_exit_plot = security_close * moving_avgs * entry * exit

# Show the plot
entry_exit_plot.opts(
    title="ETH - EMA1, EMA30, Entry and Exit Points"
)


# In[13]:


# Set initial capital
initial_capital = float(100000)

# Set the share size
share_size = 10


# In[14]:


# Buy a share position when the dual moving average crossover Signal equals 1
# Sell a share position when the dual moving average crossover Signal equals 0
signals_df['Position'] = share_size * signals_df['Signal']


# In[15]:


# Determine the points in time where a share position is bought or sold
signals_df['Entry/Exit Position'] = signals_df['Position'].diff()


# In[16]:


# Multiply the close price by the number of shares held, or the Position
signals_df['Portfolio Holdings'] = signals_df['close'] * signals_df['Position']


# In[17]:


# Subtract the amount of either the cost or proceeds of the trade from the initial capital invested
signals_df['Portfolio Cash'] = initial_capital - (signals_df['close'] * signals_df['Entry/Exit Position']).cumsum()


# In[18]:


# Calculate the total portfolio value by adding the portfolio cash to the portfolio holdings (or investments)
signals_df['Portfolio Total'] = signals_df['Portfolio Cash'] + signals_df['Portfolio Holdings']


# In[19]:


# Calculate the portfolio daily returns
signals_df['Portfolio Daily Returns'] = signals_df['Portfolio Total'].pct_change()


# In[20]:


# Calculate the portfolio cumulative returns
signals_df['Portfolio Cumulative Returns'] = (1 + signals_df['Portfolio Daily Returns']).cumprod() - 1


# In[21]:


# Print the DataFrame
signals_df.head(50)


# In[22]:


# Visualize exit position relative to total portfolio value
exit = signals_df[signals_df['Entry/Exit'] == -1.0]['Portfolio Total'].hvplot.scatter(
    color='yellow',
    marker='v',
    legend=False,
    ylabel='Total Portfolio Value',
    width=1000,
    height=400
)

# Visualize entry position relative to total portfolio value
entry = signals_df[signals_df['Entry/Exit'] == 1.0]['Portfolio Total'].hvplot.scatter(
    color='purple',
    marker='^',
    ylabel='Total Portfolio Value',
    width=1000,
    height=400
)

# Visualize the value of the total portfolio
total_portfolio_value = signals_df[['Portfolio Total']].hvplot(
    line_color='lightgray',
    ylabel='Total Portfolio Value',
    xlabel='Date',
    width=1000,
    height=400
)

# Overlay the plots
portfolio_entry_exit_plot = total_portfolio_value * entry * exit
portfolio_entry_exit_plot.opts(
    title="ETH EMAC - Total Portfolio Value",
    yformatter='%.0f'
)


# In[23]:


# Create a DataFrame that will hold portfolio evaluation metrics

# Create a list for the column name
columns = ['Backtest']

# Create a list holding the names of the new evaluation metrics
metrics = [
    'Annualized Return',
    'Cumulative Returns',
    'Annual Volatility',
    'Sharpe Ratio',
    'Sortino Ratio'
]

# Initialize the DataFrame with index set to the evaluation metrics and the column
portfolio_evaluation_df = pd.DataFrame(index=metrics, columns=columns)

# Review the DataFrame
portfolio_evaluation_df


# In[24]:


# Calculate annualized return (average daily return multipled by 252 trading days in a year)
portfolio_evaluation_df.loc['Annualized Return'] = (
    signals_df['Portfolio Daily Returns'].mean() * 252
)
portfolio_evaluation_df


# In[25]:


# Calculate cumulative return (Last value of Portfolio Cumulative Returns Column)
portfolio_evaluation_df.loc['Cumulative Returns'] = signals_df['Portfolio Cumulative Returns'][-1]
portfolio_evaluation_df


# In[26]:


# Calculate annual volatility (std dev of the daily returns column multiplied by the square root of 252 trading days)
portfolio_evaluation_df.loc['Annual Volatility'] = (
    signals_df['Portfolio Daily Returns'].std() * np.sqrt(252)
)
portfolio_evaluation_df


# In[27]:


# Calculate Sharpe ratio (Annualized Return / Annual Volatility)
portfolio_evaluation_df.loc['Sharpe Ratio'] = (
    signals_df['Portfolio Daily Returns'].mean() * 252) / (
    signals_df['Portfolio Daily Returns'].std() * np.sqrt(252)
)
portfolio_evaluation_df


# In[28]:


# Calculate downside return values (square asset's negative daily return values and then calculate the annualized return value of the asset)

# Create a DataFrame that contains the Portfolio Daily Returns column
sortino_ratio_df = signals_df[['Portfolio Daily Returns']].copy()

# Create a column to hold downside return values
sortino_ratio_df.loc[:,'Downside Returns'] = 0

# Find Portfolio Daily Returns values less than 0,
# square those values, and add them to the Downside Returns column
sortino_ratio_df.loc[sortino_ratio_df['Portfolio Daily Returns'] < 0, 'Downside Returns'] = sortino_ratio_df['Portfolio Daily Returns']**2

# Review the DataFrame
sortino_ratio_df.tail()


# In[29]:


# Calculate the Sortino ratio

# Calculate the annualized return value
annualized_return = (
    sortino_ratio_df['Portfolio Daily Returns'].mean() * 252
)

# Calculate the annualized downside standard deviation value
downside_standard_deviation = (
    np.sqrt(sortino_ratio_df['Downside Returns'].mean()) * np.sqrt(252)
)

# The Sortino ratio is reached by dividing the annualized return value
# by the downside standard deviation value
sortino_ratio = annualized_return/downside_standard_deviation

# Add the Sortino ratio to the evaluation DataFrame
portfolio_evaluation_df.loc['Sortino Ratio'] = sortino_ratio
portfolio_evaluation_df


# In[30]:


# Create a DataFrame that holds the evaluation metrics per trade

# Initialize trade evaluation DataFrame with columns
trade_evaluation_df = pd.DataFrame(
    columns=[
        'Crypto', # The name of the asset that we’re trading.
        'Entry Date', # The date that we entered (bought) the trade.
        'Exit Date', # The date that we exited (sold) the trade.
        'Tokens', # The number of shares that we executed for the trade.
        'Entry Price', # The price of the asset when we entered the trade.
        'Exit Price', # he price of the asset when we exited the trade.
        'Entry Portfolio Holding', # The cost of the trade on entry (which is the number of shares multiplied by the entry share price)
        'Exit Portfolio Holding', # The proceeds that we made from the trade on exit (which is the number of shares multiplied by the exit share price)
        'Profit/Loss'] # The profit or loss from the trade (which is the proceeds from the trade minus the cost of the trade)
)


# In[31]:


# Initialize iterative variables
entry_date = ""
exit_date = ""
entry_portfolio_holding = 0.0
exit_portfolio_holding = 0.0
share_size = 0
entry_share_price = 0.0
exit_share_price = 0.0


# In[32]:


# Loop through signal DataFrame
# If `Entry/Exit` is 1, set entry trade metrics
# Else if `Entry/Exit` is -1, set exit trade metrics and calculate profit
# Then append the record to the trade evaluation DataFrame
for index, row in signals_df.iterrows():
    if row['Entry/Exit'] == 1:
        entry_date = index
        entry_portfolio_holding = row['Portfolio Holdings']
        share_size = row['Entry/Exit Position']
        entry_share_price = row['close']

    elif row['Entry/Exit'] == -1:
        exit_date = index
        exit_portfolio_holding = abs(row['close'] * row['Entry/Exit Position'])
        exit_share_price = row['close']
        profit_loss = exit_portfolio_holding - entry_portfolio_holding
        trade_evaluation_df = trade_evaluation_df.append(
            {
                'Crypto': 'ETH',
                'Entry Date': entry_date,
                'Exit Date': exit_date,
                'Tokens': share_size,
                'Entry Price': entry_share_price,
                'Exit Price': exit_share_price,
                'Entry Portfolio Holding': entry_portfolio_holding,
                'Exit Portfolio Holding': exit_portfolio_holding,
                'Profit/Loss': profit_loss
            },
            ignore_index=True)

# Print the DataFrame
trade_evaluation_df


# In[33]:


cp = trade_evaluation_df['Profit/Loss'].sum()
cp


# In[ ]:




