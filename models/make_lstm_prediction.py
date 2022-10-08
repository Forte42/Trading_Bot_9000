def make_prediction():

	import math
	import numpy as np
	import pandas as pd
	from sklearn.preprocessing import MinMaxScaler 
	import tensorflow as tf
	from tensorflow import keras
	from tensorflow.keras import layers
	from dotenv import load_dotenv
	import os
	from sqlalchemy import create_engine
	import sqlalchemy
	import keras.backend as K
	from keras.models import load_model
	
	load_dotenv()                                                                                
	host = os.getenv("HOST")                                                                     
	dbname = os.getenv("DBNAME")                                                                 
	username = os.getenv("USERNAME")                                                             
	password = os.getenv("PASSWORD")                                                             
												     
	engine = create_engine(f"mysql+pymysql://{username}:{password}@{host}/{dbname}",)
	conn = engine.connect()     

	
	df = pd.read_sql(f"SELECT * FROM binance_btc_3m", conn)


	df['Open'] = df['Open'].astype(float)
	df['High'] = df['High'].astype(float)
	df['Low'] = df['Low'].astype(float)
	df['Close'] = df['Close'].astype(float)
	df['Volume'] = df['Volume'].astype(float)
	df['Pclose'] = df['Close'].shift(-10)
	df['Change'] = df['Close'] - df['Pclose']
	df['Updown'] = 0
	df.loc[df['Change'] > 0, 'Updown'] = 1                                                   
	df.loc[df['Change'] <= 0, 'Updown'] = 0  

	stock_data = df[['Timestamp', 'Open', 'High', 'Low', 'Close', 'Pclose', 'Volume', 'Updown', 'Number_Of_Trades']]
	print(df)
	stock_data = stock_data.dropna()
	       
	print(stock_data.tail(30))
	#quit()
	close_prices = stock_data['Pclose']
	values = close_prices.values
	training_data_len = math.ceil(len(values)* 0.8)

	scaler = MinMaxScaler(feature_range=(0,1))
	scaled_data = scaler.fit_transform(values.reshape(-1,1))

	train_data = scaled_data[0: training_data_len, :]

	x_train = []
	y_train = []

	for i in range(60, len(train_data)):
	    x_train.append(train_data[i-60:i, 0])
	    y_train.append(train_data[i, 0])
	    
	x_train, y_train = np.array(x_train), np.array(y_train)

	x_train = np.reshape(x_train, (x_train.shape[0], x_train.shape[1], 1))

	test_data = scaled_data[training_data_len-60: , : ]
	x_test = []
	y_test = values[training_data_len:]

	for i in range(60, len(test_data)):
	  x_test.append(test_data[i-60:i, 0])

	x_test = np.array(x_test)
	x_test = np.reshape(x_test, (x_test.shape[0], x_test.shape[1], 1))

	model = load_model('/home/ubuntu/Trading_Bot_9000/models/my_model.h5')

	predictions = model.predict(x_test)
	predictions = scaler.inverse_transform(predictions)
	K.clear_session()
	
	rmse = np.sqrt(np.mean(predictions - y_test)**2)
	prediction_30m = predictions[-1].astype(float)
	timestamp = df['Timestamp'].max().astype(int)
	print(timestamp)
	print(prediction_30m)
	try:
		rs = conn.execute(f'INSERT INTO lstm_3m_signal (timestamp, value) VALUES ({timestamp},{prediction_30m[0]});')
	except:
		pass
	print('end')
	conn.close()


