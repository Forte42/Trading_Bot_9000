from binance.spot import Spot                                                                                                                                                                                          
import pandas as pd                                                                                                                                                                                                    
import time                                                                                                                                                                                                            
from sqlalchemy import create_engine                                                                                                                                                                                   
import sqlalchemy                                                                                                                                                                                                      
import pymysql                                                                                                                                                                                                         
                                                                                                                                                                                                                       
#engine = create_engine()                                                                                         
                                                                                                                                                                                                                       
client = Spot()                                                                                                                                                                                                        
                                                                                                                                                                                                                       
																								   
																									       
ohlc_list = (client.klines("BTCUSDT", "15m", limit = 10000))                                                                                                                                                     
																									       
df = {}                                                                                                                                                                                                        
df = pd.DataFrame(ohlc_list)                                                                                                                                                                                   
df = df[:-1]                                                                                                                                                                                                   
																									       
df.rename(columns={0 : 'Timestamp', 1 : 'Open', 2 : 'High', 3 : 'Low', 4 : 'Close', 5 : 'Volume', 6 : 'Close_Timestamp' , 7 : 'QAV', 8 : 'Number_Of_Trades', 9 : 'TBB', 10 : 'TBQ' , 11 : 'NOT_APPLICABLE'}, inplace = True)                                                                                                                                                                                                          
	   
print(df)
