from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.schedulers.background import BlockingScheduler
import os
import time
import sys

sys.path.append('signal_generation/')
sys.path.append('models/')
scheduler = BackgroundScheduler()
#scheduler = BlockingScheduler()

import ema_1m_3m_scalp
import make_lstm_prediction

scheduler.add_job(ema_1m_3m_scalp.scalp, 'interval', seconds=.2)
scheduler.add_job(make_lstm_prediction.make_prediction, 'interval', seconds=20)






scheduler.start()

try:
	while True:
		time.sleep(2)
except (KeyboardInterrupt, SystemExit):
        # Not strictly necessary if daemonic mode is enabled but should be done if possible
        scheduler.shutdown() 
# Initialize the rest of the application here, or before the scheduler initialization
