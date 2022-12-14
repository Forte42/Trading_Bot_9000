from apscheduler.schedulers.background import BackgroundScheduler
import os
import time
import sys

sys.path.append('data_acquisition/')
scheduler = BackgroundScheduler()

import get_binance_btc_0m
import get_binance_btc_1m
import get_binance_btc_3m
import get_binance_btc_30m
import get_binance_btc_1d
import fear_greed
#import reg_model

sys.path.append('tradebot/')

import get_binance_balances 





scheduler.add_job(get_binance_btc_0m.get_binance_btc_0m_data, 'interval', seconds=.1)
scheduler.add_job(get_binance_btc_1m.get_binance_btc_1m_data, 'interval', seconds=1)
scheduler.add_job(get_binance_btc_3m.get_binance_btc_3m_data, 'interval', seconds=1)
scheduler.add_job(get_binance_btc_30m.get_binance_btc_30m_data, 'interval', seconds=10)
scheduler.add_job(get_binance_btc_1d.get_binance_btc_1d_data, 'interval', seconds=40000)
scheduler.add_job(fear_greed.get_fear_greed_daily_data, 'interval', seconds=40000)
#scheduler.add_job(reg_model.make_prediction, 'interval', seconds=60)


# Get Binance account balances

scheduler.add_job(get_binance_balances.update_binance_account_balances, 'interval', seconds=1)




scheduler.start()

try:
	while True:
		time.sleep(2)
except (KeyboardInterrupt, SystemExit):
        # Not strictly necessary if daemonic mode is enabled but should be done if possible
        scheduler.shutdown() 
# Initialize the rest of the application here, or before the scheduler initialization
