from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.schedulers.background import BlockingScheduler
import os
import time
import sys

sys.path.append('tradebot/')
scheduler = BackgroundScheduler()

import ema_trade_bot

scheduler.add_job(ema_trade_bot.trade_on_ema_signal, 'interval', seconds=.2)






scheduler.start()

try:
	while True:
		time.sleep(2)
except (KeyboardInterrupt, SystemExit):
        # Not strictly necessary if daemonic mode is enabled but should be done if possible
        scheduler.shutdown() 
# Initialize the rest of the application here, or before the scheduler initialization
