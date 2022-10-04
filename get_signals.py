from apscheduler.schedulers.background import BackgroundScheduler
import os
import time
import sys

sys.path.append('signal_generation/')
scheduler = BackgroundScheduler()

import ema_1m_3m_scalp

scheduler.add_job(ema_1m_3m_scalp.scalp, 'interval', seconds=.1)






scheduler.start()

try:
	while True:
		time.sleep(2)
except (KeyboardInterrupt, SystemExit):
        # Not strictly necessary if daemonic mode is enabled but should be done if possible
        scheduler.shutdown() 
# Initialize the rest of the application here, or before the scheduler initialization
