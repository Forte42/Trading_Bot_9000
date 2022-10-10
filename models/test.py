import math
import yfinance as yf
import numpy as np
import pandas as pd
from sklearn.preprocessing import MinMaxScaler
import matplotlib.pyplot as plt
import tensorflow as tf
from tensorflow import keras
from tensorflow.keras import layers
from dotenv import load_dotenv
import os
from sqlalchemy import create_engine
import sqlalchemy
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

print(df.tail(20))
