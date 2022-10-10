#!/usr/bin/env python
# coding: utf-8

# In[1]:


import pandas as pd
import numpy as np
import json
import hvplot.pandas
import requests
import yfinance as yf
import datetime
from pandas.tseries.offsets import DateOffset
from sklearn.preprocessing import StandardScaler


# In[2]:


# use GET method and connect to API endpoint (Fear and Greed Index API)
r = requests.get('https://api.alternative.me/fng/?limit=0')


# In[3]:


df = pd.DataFrame(r.json()['data'])


# In[4]:


# convert the value to an integer instead of an object
df['value'] = df.value.astype(int)

# convert timestamp to usable format
df['timestamp'] = pd.to_datetime(df['timestamp'], unit='s')


# In[5]:


# set index to timsetamp
df = df.set_index('timestamp')


# In[6]:


# reorganize data to oldest data points first
df = df[::-1]


# In[7]:


btc_df = yf.download('BTC-USD')[['Close']]
btc_df.index.name = 'timestamp'


# In[8]:


# Merge the two DataFrames
signals_df = df.merge(btc_df, on ='timestamp')


# In[9]:


# drop time_until_update column
signals_df = signals_df.drop(columns='time_until_update')


# In[10]:


# add percent change column and drop the null value from the shift
signals_df['Actual_Returns'] = signals_df['Close'].pct_change()

# drop the null value
signals_df = signals_df.dropna()


# In[11]:


# scale the data
visualization_df = signals_df.copy()

visualization_df = visualization_df[['value', 'Close']]

visualization_df.rename(columns={'value' : 'Fear and Greed Value', 'Close' : 'BTC Price in USD'}, inplace=True)

visualization_df


# In[12]:


# Create a StandardScaler instance
scaler = StandardScaler()
 
# Apply the scaler model to fit the data
visualization_scaled = scaler.fit_transform(visualization_df)

# Convert the scaled data to a DataFrame
compare_df = pd.DataFrame(visualization_scaled)

compare_df = compare_df.rename(columns = {0:'Fear and Greed Value', 1:'BTC Close Price'})


# In[13]:


# plot to compare
compare_df.hvplot(xlabel='Timestamp', ylabel='Fear and Greed Value', title = 'Fear and Greed Index -vs- BTC Close Price')


# In[14]:


signals_df['value_classification'].value_counts()


# In[15]:


signals_df['Actual_Returns'].hvplot()


# ## References
# * Extreme Fear = 0-25
# * Fear = 26-46 
# * Neutral = 47-54 
# * Greed = 55-75 
# * Extreme Greed = 76-100
# 
# ### Total data points = 1703
# 
# ### BTC has spent 62.42% of its time since February 2018 in fear or extreme fear territory
# 
# ### BTC has spent 28.71% of its time since February 2018 in greed or extreme greed territory
# 
# ### BTC has spent 8.87% of its time since February 2018 in neutral territory

# In[16]:


signals_df


# In[17]:


# encode the value_classifications to integers for use in machine learning models

# create the encoded value classification column
signals_df['Encoded_Class'] = 0

# encode Extreme Fear as 0
signals_df.loc[(signals_df['value_classification'] == 'Extreme Fear'), 'Encoded_Class'] = int(0)

# encode Fear as 1
signals_df.loc[(signals_df['value_classification'] == 'Fear'), 'Encoded_Class'] = int(1)

# encode Neutral as 2
signals_df.loc[(signals_df['value_classification'] == 'Neutral'), 'Encoded_Class'] = int(2)

# ecnode Greed as 3
signals_df.loc[(signals_df['value_classification'] == 'Greed'), 'Encoded_Class'] = int(3)

# encode Extreme Greed as 4
signals_df.loc[(signals_df['value_classification'] == 'Extreme Greed'), 'Encoded_Class'] = int(4)


# In[18]:


# create the entry/exit column
signals_df['Entry/Exit'] = 0

# if current row value for 'classification_int' is greater than previous row value for 'classification_int' = BUY
signals_df.loc[(signals_df['Encoded_Class'] > signals_df['Encoded_Class'].shift()), 'Entry/Exit'] = int(1)
    
# if current row value for 'classification_int' is smaller than previous row value for 'classification_int' = SELL
signals_df.loc[(signals_df['Encoded_Class'] < signals_df['Encoded_Class'].shift()), 'Entry/Exit'] = int(-1)
    
# if current row value for 'classification_int' equals previous row value for 'classification_int' = HOLD
signals_df.loc[(signals_df['Encoded_Class'] == signals_df['Encoded_Class'].shift()), 'Entry/Exit'] = int(0)

signals_df.head(50)


# In[19]:


# Visualize exit position relative to close price
exit = signals_df[signals_df['Entry/Exit'] == -1.0]['Close'].hvplot.scatter(
    color='yellow',
    marker='v',
    size=200,
    legend=False,
    ylabel='Price in $',
    width=1000,
    height=400
)

# Visualize entry position relative to close price
entry = signals_df[signals_df['Entry/Exit'] == 1.0]['Close'].hvplot.scatter(
    color='purple',
    marker='^',
    size=200,
    legend=False,
    ylabel='Price in $',
    width=1000,
    height=400
)

# Visualize close price for the investment
security_close = signals_df[['Close']].hvplot(
    line_color='lightgray',
    ylabel='Price in $',
    width=1000,
    height=400
)

# Create the overlay plot
entry_exit_plot = security_close * entry * exit

# Show the plot
entry_exit_plot.opts(
    title="BTC - Fear and Greed, Entry and Exit Points"
)


# In[20]:


# Set initial capital
initial_capital = float(100000)

# Set the coin size
coin_size = 1

# Set the commission
cost_per_trade = 0.003


# In[21]:


# daily_trade_costs = signals_df['Signal'] * cost_per_trade


# In[22]:


wallet = 0
signals_df['Signal'] = 0
i = 0

for idx, row in signals_df.iterrows():
    
    if row['Entry/Exit'] == 1:
        wallet += 1
        
    elif row['Entry/Exit'] == -1:
        wallet += -1
    
    signals_df.iloc[i, 6] = wallet
    
    i+=1

signals_df.head(50)


# In[23]:


# create a position column
signals_df['Position'] = signals_df['Signal'] * coin_size


# In[24]:


# Determine the points in time where a share position is bought or sold
signals_df['Entry/Exit Position'] = signals_df['Position'].diff()


# In[25]:


# Multiply the close price by the number of shares held, or the Position
signals_df['Portfolio Holdings'] = signals_df['Close'] * signals_df['Position']


# In[26]:


# Subtract the amount of either the cost or proceeds of the trade from the initial capital invested
signals_df['Portfolio Cash'] = initial_capital - (signals_df['Close'] * signals_df['Entry/Exit Position']).cumsum()


# In[27]:


# Calculate the total portfolio value by adding the portfolio cash to the portfolio holdings (or investments)
signals_df['Portfolio Total'] = signals_df['Portfolio Cash'] + signals_df['Portfolio Holdings']


# In[28]:


# Calculate the portfolio daily returns
signals_df['Portfolio Daily Returns'] = signals_df['Portfolio Total'].pct_change()


# In[29]:


# Calculate the portfolio cumulative returns
signals_df['Portfolio Cumulative Returns'] = (1 + signals_df['Portfolio Daily Returns']).cumprod() - 1


# In[30]:


# Print the DataFrame
signals_df.tail()


# In[31]:


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


# In[32]:


# Calculate annualized return (average daily return multipled by 252 trading days in a year)
portfolio_evaluation_df.loc['Annualized Return'] = (
    signals_df['Portfolio Daily Returns'].mean() * 252
)
portfolio_evaluation_df


# In[33]:


# Calculate cumulative return (Last value of Portfolio Cumulative Returns Column)
portfolio_evaluation_df.loc['Cumulative Returns'] = signals_df['Portfolio Cumulative Returns'][-1]
portfolio_evaluation_df


# In[34]:


# Calculate annual volatility (std dev of the daily returns column multiplied by the square root of 252 trading days)
portfolio_evaluation_df.loc['Annual Volatility'] = (
    signals_df['Portfolio Daily Returns'].std() * np.sqrt(252)
)
portfolio_evaluation_df


# In[35]:


# Calculate Sharpe ratio (Annualized Return / Annual Volatility)
portfolio_evaluation_df.loc['Sharpe Ratio'] = (
    signals_df['Portfolio Daily Returns'].mean() * 252) / (
    signals_df['Portfolio Daily Returns'].std() * np.sqrt(252)
)
portfolio_evaluation_df


# In[36]:


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


# In[37]:


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


# In[46]:


# # Create a DataFrame that holds the evaluation metrics per trade

# # Initialize trade evaluation DataFrame with columns
# trade_evaluation_df = pd.DataFrame(
#     columns=[
#         'Crypto', # The name of the asset that we’re trading.
#         'Entry Date', # The date that we entered (bought) the trade.
#         'Exit Date', # The date that we exited (sold) the trade.
#         'Tokens', # The number of shares that we executed for the trade.
#         'Entry Price', # The price of the asset when we entered the trade.
#         'Exit Price', # he price of the asset when we exited the trade.
#         'Entry Portfolio Holding', # The cost of the trade on entry (which is the number of shares multiplied by the entry share price)
#         'Exit Portfolio Holding', # The proceeds that we made from the trade on exit (which is the number of shares multiplied by the exit share price)
#         'Profit/Loss'] # The profit or loss from the trade (which is the proceeds from the trade minus the cost of the trade)
# )


# In[45]:


# # Initialize iterative variables
# entry_date = ""
# exit_date = ""
# entry_portfolio_holding = 0.0
# exit_portfolio_holding = 0.0
# share_size = 0
# entry_share_price = 0.0
# exit_share_price = 0.0


# In[44]:


# # Loop through signal DataFrame
# # If `Entry/Exit` is 1, set entry trade metrics
# # Else if `Entry/Exit` is -1, set exit trade metrics and calculate profit
# # Then append the record to the trade evaluation DataFrame
# for index, row in signals_df.iterrows():
#     if row['Entry/Exit'] == 1:
#         entry_date = index
#         entry_portfolio_holding = row['Portfolio Holdings']
#         share_size = row['Entry/Exit Position']
#         entry_share_price = row['Close']

#     elif row['Entry/Exit'] == -1:
#         exit_date = index
#         exit_portfolio_holding = abs(row['Close'] * row['Entry/Exit Position'])
#         exit_share_price = row['Close']
#         profit_loss = exit_portfolio_holding - entry_portfolio_holding
#         trade_evaluation_df = trade_evaluation_df.append(
#             {
#                 'Crypto': 'BTC',
#                 'Entry Date': entry_date,
#                 'Exit Date': exit_date,
#                 'Tokens': share_size,
#                 'Entry Price': entry_share_price,
#                 'Exit Price': exit_share_price,
#                 'Entry Portfolio Holding': entry_portfolio_holding,
#                 'Exit Portfolio Holding': exit_portfolio_holding,
#                 'Profit/Loss': profit_loss
#             },
#             ignore_index=True)

# # Print the DataFrame
# trade_evaluation_df


# In[43]:


# cp = trade_evaluation_df['Profit/Loss'].sum()
# cp


# In[ ]:




