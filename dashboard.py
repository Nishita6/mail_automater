import streamlit as st
import pandas as pd
import json
import threading
import time as t
import pytz
import os
from datetime import datetime, time

from modules.google_sheets import get_google_sheet_data
from app import run_email_campaign_automated
from followup_scheduler import run_followups


# =========================
# SESSION STATE INIT
# =========================
if "sheet_url" not in st.session_state:
    st.session_state.sheet_url = ""

if "scheduler_started" not in st.session_state:
    st.session_state.scheduler_started = False


# =========================
# BACKGROUND SCHEDULER
# =========================
def background_scheduler(email_creds):

    IST = pytz.timezone('Asia/Kolkata')

    while True:
        jobs = []

        try:
            if os.path.exists("scheduled_jobs.json"):
                with open("scheduled_jobs.json", "r") as f:
                    jobs = json.load(f)
        except:
            jobs = []

        now = datetime.now(IST).replace(tzinfo=None)
        updated = False

        for job in jobs:
            if job.get("status") == "pending":

                schedule_time = datetime.strptime(
                    job["schedule_time"],
                    "%Y-%m-%d %H:%M:%S"
                )

                if now >= schedule_time:
                    try:
                        run_email_campaign_automated(
                            creds=email_creds,
                            url=job["sheet_url"]
                        )

                        job["status"] = "completed"
                        updated = True

                        print(f"✅ Job completed: {job['sheet_url']}")

                    except Exception as e:
                        print(f"❌ Job failed: {e}")

        if updated:
            with open("scheduled_jobs.json", "w") as f:
                json.dump(jobs, f, indent=4)

        t.sleep(30)


# =========================
# START SCHEDULER ONCE
# =========================
def start_scheduler_once():
    if st.session_state.scheduler_started:
        return

    creds = {
        "EMAIL": st.secrets["EMAIL"],
        "APP_PASSWORD": st.secrets["APP_PASSWORD"]
    }

    thread = threading.Thread(
        target=background_scheduler,
        args=(creds,),
        daemon=True
    )
    thread.start()

    st.session_state.scheduler_started = True
    st.success("🚀 Scheduler started")


start_scheduler_once()


# =========================
# UI
# =========================
st.title("Cold Email Dashboard")


# =========================
# INPUT SHEET URL
# =========================
sheet_url = st.text_input(
    "Paste Google Sheet URL",
    value=st.session_state.sheet_url
)

if sheet_url:
    st.session_state.sheet_url = sheet_url


# =========================
# LOAD DATA (ONLY ONCE)
# =========================
df = pd.DataFrame()

if st.session_state.sheet_url:
    try:
        df = get_google_sheet_data(st.session_state.sheet_url)
        st.success("Google Sheet Connected")
    except Exception as e:
        st.exception(e)


# =========================
# LOAD CAMPAIGN HISTORY
# =========================
campaign_file = "campaign_history.json"

try:
    with open(campaign_file, "r") as f:
        previous_campaigns = json.load(f)
except:
    previous_campaigns = []


# =========================
# SIDEBAR HISTORY
# =========================
st.sidebar.title("Previous Campaigns")

for i, campaign in enumerate(previous_campaigns):
    if st.sidebar.button(f"Campaign {i+1}"):
        st.session_state.sheet_url = campaign["sheet_url"]
        st.rerun()


# =========================
# SAVE CAMPAIGN HISTORY
# =========================
if sheet_url and sheet_url not in [c["sheet_url"] for c in previous_campaigns]:
    previous_campaigns.append({
        "sheet_url": sheet_url,
        "added_on": str(datetime.now())
    })

    with open(campaign_file, "w") as f:
        json.dump(previous_campaigns, f, indent=4)


# =========================
# VALIDATION
# =========================
if not df.empty:

    required = ["name", "company", "email", "domain", "status"]
    missing = [c for c in required if c not in df.columns]

    if missing:
        st.error(f"Missing columns: {missing}")
        st.stop()


# =========================
# DISPLAY DATA
# =========================
if not df.empty:

    st.subheader("Lead Data")
    st.dataframe(df, use_container_width=True)

    # =========================
    # METRICS
    # =========================
    total = len(df)
    pending = len(df[df["status"] == "pending"])
    sent = len(df[df["status"] == "sent"])

    followups = 0
    if "followup_sent" in df.columns:
        followups = len(df[df["followup_sent"].astype(str).str.lower() == "yes"])

    c1, c2, c3, c4 = st.columns(4)

    c1.metric("Total Leads", total)
    c2.metric("Pending", pending)
    c3.metric("Sent", sent)
    c4.metric("Followups", followups)

    # =========================
    # CHART
    # =========================
    st.subheader("Status Distribution")
    st.bar_chart(df["status"].value_counts())


# =========================
# ACTION BUTTONS
# =========================
col1, col2 = st.columns(2)

with col1:
    if st.button("Send Pending Emails"):
        try:
            run_email_campaign_automated(
                creds={
                    "EMAIL": st.secrets["EMAIL"],
                    "APP_PASSWORD": st.secrets["APP_PASSWORD"]
                },
                url=st.session_state.sheet_url
            )
            st.success("Emails sent")
            st.rerun()
        except Exception as e:
            st.exception(e)

with col2:
    if st.button("Run Followups"):
        try:
            run_followups()
            st.success("Followups sent")
            st.rerun()
        except Exception as e:
            st.exception(e)


# =========================
# SCHEDULER INPUT
# =========================
st.subheader("Schedule Emails")

with st.expander("Open Scheduler"):

    schedule_date = st.date_input("Date")
    hour = st.selectbox("Hour", list(range(24)))
    minute = st.selectbox("Minute", ["00","05","10","15","20","25","30","35","40","45","50","55"])

    schedule_time = time(hour, int(minute))

    if st.button("Schedule"):

        scheduled_datetime = datetime.combine(schedule_date, schedule_time)

        try:
            if os.path.exists("scheduled_jobs.json"):
                with open("scheduled_jobs.json", "r") as f:
                    jobs = json.load(f)
            else:
                jobs = []
        except:
            jobs = []

        jobs.append({
            "sheet_url": st.session_state.sheet_url,
            "schedule_time": scheduled_datetime.strftime("%Y-%m-%d %H:%M:%S"),
            "status": "pending"
        })

        with open("scheduled_jobs.json", "w") as f:
            json.dump(jobs, f, indent=4)

        st.success("Email scheduled")


# =========================
# SHOW JOBS
# =========================
st.subheader("Scheduled Jobs")

try:
    if os.path.exists("scheduled_jobs.json"):
        with open("scheduled_jobs.json", "r") as f:
            jobs = json.load(f)

        st.dataframe(pd.DataFrame(jobs), use_container_width=True)
    else:
        st.info("No scheduled jobs")
except:
    st.info("No scheduled jobs")