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
from sklearn.preprocessing import StandardScaler, OneHotEncoder
from imblearn.over_sampling import RandomOverSampler
from sklearn.svm import SVC
from sklearn.metrics import classification_report


# In[2]:


# use GET method and connect to API endpoint (Fear and Greed Index API)
r = requests.get('https://api.alternative.me/fng/?limit=0')


# In[3]:


# convert JSON data to Pandas DataFrame
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


# get BTC close prices from yahoo finance
btc_df = yf.download('BTC-USD')[['Close']]

# rename the index from Date to timestamp
btc_df.index.name = 'timestamp'


# In[8]:


# merge the two DataFrames
signals_df = df.merge(btc_df, on ='timestamp')


# In[9]:


# drop time_until_update column
signals_df = signals_df.drop(columns='time_until_update')


# In[10]:


# calculate actual returns
signals_df['Actual_Returns'] = signals_df['Close'].pct_change()

# drop null value
signals_df = signals_df.dropna()


# In[11]:


# prepare to encode categorical features
categorical_vairables = ['value_classification']


# In[12]:


# instantiate the encoder
enc = OneHotEncoder(sparse=False)


# In[13]:


# encode the data
encoded_data = enc.fit_transform(signals_df[categorical_vairables])


# In[14]:


# convert the encoded data to a DataFrame
encoded_df = pd.DataFrame(
    encoded_data,
    columns = enc.get_feature_names(categorical_vairables)
)

encoded_df


# In[15]:


# separate the categorical data from the numerical data
numerical_df = signals_df.drop(columns='value_classification')


# In[16]:


# reset the index
numerical_df = numerical_df.reset_index()


# In[17]:


# visualize the data
numerical_df.hvplot.scatter(x='Close', y='value')


# In[18]:


# Combine the DataFrames that contain the encoded categorical data and the numerical data
combined_df = pd.concat(
    [
        numerical_df,
        encoded_df
    ],
    axis=1
)

# Reveiw the DataFrame
combined_df.head()


# In[19]:


# set the index
combined_df = combined_df.set_index('timestamp')


# In[20]:


# create the target signal for classification models
combined_df['Signal'] = 0

# signal is 1 when the actual return is positive
combined_df.loc[(combined_df['Actual_Returns'] >= 0), 'Signal'] = 1

# signal is -1 when the actual return is negative
combined_df.loc[(combined_df['Actual_Returns'] < 0), 'Signal'] = 0


# In[21]:


# view the DataFrame
combined_df


# ## Machine Learning - Split, Scale, Resample Data
# ---

# In[22]:


# separate the target data
y = combined_df['Signal']

# drop the first row to match the feature data
y = y.iloc[1:]


# In[23]:


# shift actual returns down one row so machine learning model is associating next days return with current day data (predict one day in the future)
X = combined_df[[
    'value', 
    'value_classification_Extreme Fear', 
    'value_classification_Extreme Greed', 
    'value_classification_Fear', 
    'value_classification_Greed', 
    'value_classification_Neutral'
]].shift().dropna().copy()


# In[24]:


# Split the data into training and testing datasets
y.value_counts()


# In[25]:


# Select the start of the training period
training_begin = X.index.min()
print(training_begin)


# In[26]:


# Ending period for the training data:
training_end = X.index.min() + DateOffset(months=45)
print(training_end)


# In[27]:


# Generate the X_train and y_train DataFrames
X_train = X.loc[training_begin:training_end]
y_train = y.loc[training_begin:training_end]


# In[28]:


# Generate the X_test and y_test DataFrames
X_test = X.loc[training_end:]
y_test = y.loc[training_end:]


# In[29]:


# Create a StandardScaler instance
scaler = StandardScaler()

# Fit the scaler to the features training dataset
X_scaler = scaler.fit(X_train)

# Fit the scaler to the features training dataset
X_train_scaled = X_scaler.transform(X_train)
X_test_scaled = X_scaler.transform(X_test)


# In[30]:


# Use RandomOverSampler to resample the datase
ros = RandomOverSampler(random_state=1)
X_resampled, y_resampled = ros.fit_resample(X_train_scaled, y_train)


# ## Machine Learning - Create, Fit, and Test the Model
# ---

# In[31]:


# SVC Model
# model = SVC()# probability=True
model = SVC(probability=True)


# In[32]:


# Fit the model to the data using X_train_scaled and y_train
model = model.fit(X_resampled, y_resampled)


# In[33]:


# Use the trained model to predict the trading signals for the training data.
training_signal_predictions_SVC = model.predict(X_resampled)

# Evaluate the model using a classification report
training_report = classification_report(y_resampled, training_signal_predictions_SVC)
print(training_report)


# In[34]:


# Use the trained model to predict the trading signals for the testing data.
testing_signal_predictions_SVC = model.predict(X_test_scaled)


# In[35]:


# Create a new empty predictions DataFrame
test_predictions_SVC_df = pd.DataFrame(index=X_test.index)
test_predictions_SVC_df['predicted_returns'] = testing_signal_predictions_SVC
test_predictions_SVC_df['predicted_returns'].value_counts()


# In[36]:


# Add in actual returns and calculate trading returns
test_predictions_SVC_df['actual_returns'] = combined_df['Actual_Returns']
test_predictions_SVC_df['trading_algorithm_returns'] = test_predictions_SVC_df['actual_returns'] * test_predictions_SVC_df['predicted_returns']
test_predictions_SVC_df


# In[37]:


# generate cumulative returns columns
test_predictions_SVC_df['cumulative_returns_actual'] = (1 + test_predictions_SVC_df['actual_returns']).cumprod()

test_predictions_SVC_df['cumulative_returns_algo'] = (1 + test_predictions_SVC_df['trading_algorithm_returns']).cumprod()

test_predictions_SVC_df


# In[38]:


# Calculate and plot the cumulative returns for the `actual_returns` and the `trading_algorithm_returns`
test_predictions_SVC_df[['cumulative_returns_actual', 'cumulative_returns_algo']].hvplot()

