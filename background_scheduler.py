import json

import os

import threading

import time

from datetime import datetime


def run_scheduler():

    print("Background Scheduler Started...")

    while True:

        try:

            with open(
                "scheduled_jobs.json",
                "r"
            ) as file:

                jobs = json.load(file)

        except:

            jobs = []

        updated_jobs = []

        for job in jobs:

            try:

                schedule_time = datetime.strptime(

                    job["schedule_time"],

                    "%Y-%m-%d %H:%M:%S"
                )

                current_time = datetime.now()
                if (

                    current_time >= schedule_time

                    and

                    job["status"] == "pending"
                ):

                    with open(
                        "sheet_url.txt",
                        "w"
                    ) as file:

                        file.write(
                            job["sheet_url"]
                        )

                    print(
                        "Sending Scheduled Emails..."
                    )

                    os.system(
                        "python app.py"
                    )

                    os.system(
                        "python followup_scheduler.py"
                    )

                    job["status"] = "completed"

                    print(
                        "Scheduled Job Completed"
                    )

            except Exception as e:

                print(e)

            updated_jobs.append(job)

        with open(
            "scheduled_jobs.json",
            "w"
        ) as file:

            json.dump(
                updated_jobs,
                file,
                indent=4
            )

        time.sleep(30)


scheduler_thread = threading.Thread(

    target=run_scheduler,

    daemon=True
)

scheduler_thread.start()