from apscheduler.schedulers.blocking import (
    BlockingScheduler
)

import os

scheduler = BlockingScheduler()

# Run every 24 hours
scheduler.add_job(

    lambda: os.system(
        "python followup_scheduler.py"
    ),

    trigger='interval',

    hours=24
)

print(
    "Scheduler Started..."
)

scheduler.start()