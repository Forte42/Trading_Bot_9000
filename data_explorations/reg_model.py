import pandas as pd
import numpy as np
from pandas.tseries.offsets import DateOffset
import os
import requests
import datetime
import yfinance as yf
from sklearn.preprocessing import MinMaxScaler
from sklearn.preprocessing import MinMaxScaler
import tensorflow as tf
from tensorflow.keras.layers import Dense
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import LSTM
#import matplotlib.pyplot as plt
from numpy.lib import math
from tensorflow.keras.layers import Dropout
from tensorflow.keras.layers import TimeDistributed
from tensorflow.keras.layers import Bidirectional
from pathlib import Path
from keras.models import load_model
#get_ipython().run_line_magic('matplotlib', 'inline')


# ## Data Retreival/Formatting


# Pull data

btc_df = yf.download('BTC-USD', start='2021-09-01',interval='1h')[['Open','High','Low','Volume','Close']]
btc_df.index.name = 'timestamp'

print(btc_df)

print(btc_df.dtypes)


# Shift X data to predict price 24 hours in the future
btc_df[['Open', 'High','Low','Volume','Close']]=btc_df[['Open', 'High','Low','Volume','Close']].shift(24)
print(btc_df.head())

# Drop rows w/ empty values
btc_df = btc_df.dropna()
print(btc_df.head())




# ### Splitting data into 3D Tensors


# Split test and train data

split_ratio=.7
train_count=int(len(btc_df)*.7)

train=btc_df.iloc[:train_count]
test=btc_df.iloc[train_count:]


# In[168]:


# Create a MinMaxScaler instance
scaler = MinMaxScaler()

# Fit the scaler to the features training dataset
train_scaled = scaler.fit_transform(train)

train_scaled


# In[169]:


# Scale test data
test_scaled = scaler.fit_transform(test)

test_scaled


# In[170]:


# Set global candles variable
candles=60

# Create X training set
X_train = []

for i in range(len(train_scaled) - candles):
    X_train.append(train_scaled[:,:4][i:i+candles])

X_train = np.array(X_train)
X_train.shape


# In[171]:


# Create y training set
y_train = []

for i in range(len(train_scaled) - candles):
    y_train.append(train_scaled[:,(4)][i+candles])

y_train = np.array(y_train)
y_train.shape


# In[172]:


# Create X test set
X_test = []

for i in range(len(test_scaled) - candles):
    X_test.append(test_scaled[:,:4][i  : i+candles])

X_test = np.array(X_test)
X_test.shape


# In[173]:


# Create y test set
y_test = []

for i in range(len(test_scaled) - candles):
    y_test.append(test_scaled[:,(4)][i+candles])

y_test = np.array(y_test)
y_test.shape

model = load_model('/home/ubuntu/Trading_Bot_9000/models/regr_nn.h5')

print(model)
## ## Model Creation
#
## In[174]:
#
#
## Create the Sequential model instance
#regr_nn = Sequential()
#
## Define the number of neurons in the output layer
#number_output_neurons = 1
#
##Define the number of hidden nodes for the first hidden layer
#hidden_nodes_layer1 = 64
#
## Define hidden nodes for all hidden layers
#hidden_nodes = 64
#display(hidden_nodes)
#
## Review the number hidden nodes in the first layer
#display(hidden_nodes_layer1)
#
##Define the number of hidden nodes for the second hidden layer
#hidden_nodes_layer2 = 64
#
## Review the number hidden nodes in the second layer
#display(hidden_nodes_layer2)
#
#
## In[175]:
#
#
## Add the first hidden layer
#regr_nn.add(LSTM(units=hidden_nodes_layer1, return_sequences=True, input_shape=(candles,(len(btc_df.columns)-1))))
#
#
## In[176]:
#
#
## # Add dropout layer
#regr_nn.add(Dropout(rate=0.2))
#
#
## In[177]:
#
#
##Add the second hidden layer
#regr_nn.add(LSTM(units=hidden_nodes, return_sequences=True))
#
#
## In[178]:
#
#
## # Add dropout layer
#regr_nn.add(Dropout(rate=0.2))
#
#
## In[179]:
#
#
## #Add the third hidden layer
#regr_nn.add(LSTM(units=hidden_nodes))
#
#
## In[180]:
#
#
## # Add dropout layer
## regr_nn.add(Dropout(rate=0.2))
#
#
## In[181]:
#
#
## Add Dense layer
## regr_nn.add(Dense(units=6, activation='relu'))
#
#
## In[182]:
#
#
## Add the output layer to the model specifying the number of output neurons and activation function
#regr_nn.add(Dense(units=1,  activation='linear'))
#
#
## In[183]:
#
#
## Display the Sequential model summary, subclassed model requires build
#regr_nn.build(X_train.shape)
#regr_nn.summary()
#
#
## In[184]:
#
#
## Compile the Sequential model
#
#regr_nn.compile(loss='mean_squared_error', optimizer='adam')
#
#
## In[185]:
#
#
## Fit the model using epochs and the training data
#regr_model=regr_nn.fit(X_train, y_train, epochs=20, validation_split=.01)
#
#
## In[186]:
#
#
## Train vs test for loss
#plt.plot(regr_model.history["loss"])
#plt.plot(regr_model.history["val_loss"])
#plt.title("Training Vs. Validation 2 LSTM, w/ Dropout")
#plt.legend(["loss", "val_loss"])
#plt.show()
#
#
## In[187]:
#
#
# Make model predictionis

y_pred=model.predict(X_test)

unscaler = test_scaled[:(len(test_scaled) - candles),:4]

unscaler = np.concatenate((unscaler, y_pred), axis=1)

y_pred = scaler.inverse_transform(unscaler)

print(y_pred)
#
#
#
## Plot prediction results
#plt.plot(range(len(y_test)), (y_test))
#plt.plot(range(len(y_test)), (y_pred))
#plt.legend(["test", "prediction"])
#
#
## In[189]:
#
#
## Set the file path for the first regression model
#file_path = Path('Models/regr_nn.h5')
#
## Export your model to a HDF5 file
#regr_nn.save(file_path)
#
#
## In[ ]:
#
#
#
#
