# Import the required libraries
import pandas as pd
import numpy as np
import json
import requests
import yfinance as yf
import datetime

# Use GET method and connect to API endpoint (Fear and Greed Index API)
r = requests.get('https://api.alternative.me/fng/?limit=0')

# Create a DataFrame
df = pd.DataFrame(r.json()['data'])

# Convert the value to an integer instead of an object
df['value'] = df.value.astype(int)

# Convert timestamp to usable format
df['timestamp'] = pd.to_datetime(df['timestamp'], unit='s')

# Set index to timsetamp
df = df.set_index('timestamp')

# Reorganize data to oldest data points first
df = df[::-1]

# Download BTC close prices
btc_df = yf.download('BTC-USD')[['Close']]
btc_df.index.name = 'timestamp'

# Merge the two DataFrames
signals_df = df.merge(btc_df, on ='timestamp')

# drop time_until_update column
signals_df = signals_df.drop(columns='time_until_update')

# add percent change column
signals_df['Actual_Returns'] = signals_df['Close'].pct_change()

# drop the null value
signals_df = signals_df.dropna()


# encode the value_classifications as integers
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


# create the entry/exit column
signals_df['Entry/Exit'] = 0

# if current row value for 'classification_int' is greater than previous row value for 'classification_int' = BUY
signals_df.loc[(signals_df['Encoded_Class'] > signals_df['Encoded_Class'].shift()), 'Entry/Exit'] = int(1)
    
# if current row value for 'classification_int' is smaller than previous row value for 'classification_int' = SELL
signals_df.loc[(signals_df['Encoded_Class'] < signals_df['Encoded_Class'].shift()), 'Entry/Exit'] = int(-1)
    
# if current row value for 'classification_int' equals previous row value for 'classification_int' = HOLD
signals_df.loc[(signals_df['Encoded_Class'] == signals_df['Encoded_Class'].shift()), 'Entry/Exit'] = int(0)