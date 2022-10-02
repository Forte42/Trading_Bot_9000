import pandas_datareader as web # to read data from web                                                                                                               
import pandas as pd                                                                                                                                                   
import numpy as np                                                                                                                                                    
# import the data                                                                                                                                                     
APPL_data= web.DataReader('AAPL',data_source="yahoo",start='2015-01-01',end='2021-09-30')                                                                             
APPL_data.head()                                                                                                                                                      
                                                                                                                                                                      
# Split into train and test:                                                                                                                                          
data_to_train = APPL_data[:1530]                                                                                                                                      
data_to_test = APPL_data[1530:]                                                                                                                                       
aapl_data= APPL_data.iloc[: , 3:4]                                                                                                                                    
aapl_data.head()                                                                                                                                                      
                                                                                                                                                                      
## We want to create a numpy arrary not a vector                                                                                                                      
trainig_set= aapl_data.iloc[:1530,:].values                                                                                                                           
                                                                                                                                                                      
test_set= aapl_data.iloc[1530:,:].values                                                                                                                              
                                                                                                                                                                      
# Feature scalling, Here we will do normalizatioin                                                                                                                    
from sklearn.preprocessing import MinMaxScaler                                                                                                                        
sc= MinMaxScaler(feature_range=(0,1))                                                                                                                                 
trainig_set_scaled= sc.fit_transform(trainig_set)                                                                                                                     
                                                                                                                                                                      
# Create a data structure with 60 timesteps and 1 output                                                                                                              
X_train=[] #Independent variables                                                                                                                                     
y_train= [] # Dependent variables                                                                                                                                     
# I am going to append past 60 days data                                                                                                                              
for i in range(60,1530):                                                                                                                                              
    X_train.append(trainig_set_scaled[i-60:i,0]) # Appending prevois 60 days data not including 60                                                                    
    y_train.append(trainig_set_scaled[i,0])                                                                                                                           
                                                                                                                                                                      
X_train, y_train= np.array(X_train), np.array(y_train)                                                                                                                
                                                                                                                                                                      
# Importing the Keras libraries and packages                                                                                                                          
import tensorflow as tf                                                                                                                                               
from tensorflow.keras.models import Sequential                                                                                                                        
from tensorflow.keras.layers import Dense, Dropout, LSTM                                                                                                              
                                                                                                                                                                      
#  Initialising the RNN                                                                                                                                               
model= Sequential()                  

# Adding first LSTM layer and some dropout Dropout regularisation                                                                                                     
model.add(LSTM(units=100,return_sequences=True, input_shape=(X_train.shape[1],1)))                                                                                    
model.add(Dropout(rate=0.2))                                                                                                                                          
                                                                                                                                                                      
# Adding second LSTM layer and some dropout Dropout regularisation                                                                                                    
model.add(LSTM(units=100,return_sequences=True))                                                                                                                      
model.add(Dropout(rate=0.2))                                                                                                                                          
                                                                                                                                                                      
# Adding third LSTM layer and some dropout Dropout regularisation                                                                                                     
model.add(LSTM(units=100,return_sequences=True))                                                                                                                      
model.add(Dropout(rate=0.2))                                                                                                                                          
                                                                                                                                                                      
# Adding fourth LSTM layer and some dropout Dropout regularisation                                                                                                    
model.add(LSTM(units=100,return_sequences=True))                                                                                                                      
model.add(Dropout(rate=0.2))                                                                                                                                          
                                                                                                                                                                      
# Adding fifth LSTM layer and some dropout Dropout regularisation                                                                                                     
model.add(LSTM(units=100))                                                                                                                                            
model.add(Dropout(rate=0.2))                                                                                                                                          
                                                                                                                                                                      
# Adding the Output Layer                                                                                                                                             
model.add(Dense(units=1))                                                                                                                                             
                                                                                                                                                                      
# Compiling the Model                                                                                                                                                 
# Because we're doing regression hence mean_squared_error                                                                                                             
model.compile(loss='mean_squared_error', optimizer='adam')                                                                                                            
                                                                                                                                                                      
print(model.summary())                                                                                                                                                
                                                                                                                                                                      
# Fitting the model to the Training set                                                                                                                               
history=model.fit(X_train,y_train,epochs=100,batch_size=32)                                                                                                           
                                                                                                                                                                      
# Hence we will concatenate the dataset and then scale them                                                                                                           
data_total= pd.concat([train_data['Close'], test_data['Close']],  axis=0)                                                                                             
inputs= data_total[len(data_total)-len(test_data)-60:].values                                                                                                         
inputs = inputs.reshape(-1,1)                                                                                                                                         
inputs = sc.transform(inputs)                                                                                                                                         
                                                                                                                                                                      
X_test = []                                                                                                                                                           
for i in range(60, 230):                                                                                                                                              
    X_test.append(inputs[i-60:i, 0])                                                                                                                                  
                                                                                                                                                                      
X_test = np.array(X_test)                                                                                                                                             
# 3D format                                                                                                                                                           
X_test = np.reshape(X_test, (X_test.shape[0], X_test.shape[1], 1))                                                                                                    
                                                                                                                                                                      
#preict the model                                                                                                                                                     
predicted_stock_price = model.predict(X_test)    
