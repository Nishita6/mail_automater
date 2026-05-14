import json
import time

from datetime import datetime

from app import run_email_campaign

def start_scheduler():

    print(
        "Background Scheduler Started..."
    )

    while True:

        try:

            with open(
                "scheduled_jobs.json",
                "r"
            ) as file:

                jobs = json.load(file)

        except:

            jobs = []

        updated = False

        for job in jobs:

            if job["status"] == "pending":

                schedule_time = datetime.strptime(

                    job["schedule_time"],

                    "%Y-%m-%d %H:%M:%S"
                )

                if datetime.now() >= schedule_time:

                    try:

                        run_email_campaign()

                        job["status"] = "completed"

                    except Exception as e:

                        print(e)

                        job["status"] = "failed"

                    updated = True

        if updated:

            with open(
                "scheduled_jobs.json",
                "w"
            ) as file:

                json.dump(
                    jobs,
                    file,
                    indent=4
                )

        time.sleep(30)