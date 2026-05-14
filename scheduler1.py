import json
import time

from datetime import datetime

from app import run_email_campaign

# =========================
# START SCHEDULER
# =========================

def start_scheduler():

    print(
        "Background Scheduler Started..."
    )

    while True:

        print(
            "Checking scheduled jobs..."
        )

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

            print(job)

            if job["status"] == "pending":

                schedule_time = datetime.strptime(

                    job["schedule_time"],

                    "%Y-%m-%d %H:%M:%S"
                )

                print(
                    f"Current Time: {datetime.now()}"
                )

                print(
                    f"Scheduled Time: {schedule_time}"
                )

                # =========================
                # RUN CAMPAIGN
                # =========================

                if datetime.now() >= schedule_time:

                    print(
                        "Running Scheduled Campaign..."
                    )

                    try:

                        run_email_campaign()

                        job["status"] = "completed"

                        print(
                            "Campaign Completed"
                        )

                    except Exception as e:

                        print(e)

                        job["status"] = "failed"

                    updated = True

        # =========================
        # SAVE UPDATED JOBS
        # =========================

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

        # =========================
        # WAIT 30 SECONDS
        # =========================

        time.sleep(30)