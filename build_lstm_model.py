import os
os.environ['CUDA_VISIBLE_DEVICES'] ="0"
import pandas as pd
import numpy as np
from pandas.tseries.offsets import DateOffset
#import os
import requests
import datetime
from sklearn.preprocessing import MinMaxScaler
from sklearn.preprocessing import StandardScaler
import tensorflow as tf
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense, Dropout, LSTM  
from tensorflow.keras.layers import Dense
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import LSTM
from numpy.lib import math
from dotenv import load_dotenv
from sqlalchemy import create_engine
import sqlalchemy
import pymysql
import make_binance_btc_ohlcv as makedf                                                                                                     
                                                                                                                                            
df = makedf.return_dataframe('1d')                                                                                                          
print(df) 

df = df.reset_index()
df = df.set_index('Timestamp')
df = df[['Open','High','Low','Close','Volume', 'Number_Of_Trades', 'VWAP']]
df['Actual_Returns'] = df['Close'].pct_change()
df = df.dropna()
df['Signal'] = 0.0
df.loc[(df['Actual_Returns'] >= 0), 'Signal'] = 1
X=df[['Open', 'High', 'Low','Close','Volume','Number_Of_Trades']].shift().dropna()
# Create a StandardScaler instance
scaler = StandardScaler()
# Fit the scaler to the features training dataset
X_scaled = scaler.fit_transform(X)
# get array representation of dataframe
dataset = df.values
# get number of rows to train the model on
training_data_len = math.ceil(len(dataset) * 0.8)
# create train dataset
train_data = X_scaled[0:training_data_len, :]
# Create blank array
X_train = []
candles = 60
for i in range(candles, len(train_data)):
	X_train.append(train_data[i-candles:i, 0:6])


# create test dataset
test_data = X_scaled[training_data_len - candles: , :]

# Create blank array
X_test = []

for i in range(candles, len(test_data)):
	X_test.append(test_data[i-candles:i, 0:6])
X_train = np.array(X_train)
X_test = np.array(X_test)

print(len(X_train))
print(len(X_test))
print(X_train)

# Create the target set selecting the Signal column and assiging it to y
y = df['Signal']

# Drop first row
y = y.iloc[1:-60]

# Splitting Y data

y_train = y.iloc[0:len(X_train)]
y_test = y.iloc[len(X_train):]

# Define the the number of inputs (features) to the model
number_input_features = len(X.columns)

# Review the number of features
number_input_features

# Create the Sequential model instance
nn = Sequential()

# Define the number of neurons in the output layer
number_output_neurons = 1

# Define the number of hidden nodes for the first hidden layer
# hidden_nodes_layer1 = (number_input_features + 1) // 2
hidden_nodes_layer1 = 64

# Define the number of hidden nodes for the second hidden layer
# hidden_nodes_layer2 = (hidden_nodes_layer1 + 1) //2
hidden_nodes_layer2 = 64

# Add the first hidden layer
nn.add(LSTM(units=hidden_nodes_layer1, return_sequences=True, input_dim=number_input_features))
