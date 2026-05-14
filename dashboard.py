import streamlit as st
import pandas as pd
import json
import threading
import background_scheduler
from datetime import datetime, time

from app import run_email_campaign

from followup_scheduler import (
    run_followups
)

from modules.google_sheets import (
    get_google_sheet_data
)

# =========================
# PAGE CONFIG
# =========================

st.set_page_config(

    page_title="Cold Email Dashboard",

    layout="wide"
)

# =========================
# TITLE
# =========================

st.title(
    "Cold Email Automation Dashboard"
)

# =========================
# START BACKGROUND SCHEDULER
# =========================

if "scheduler_started" not in st.session_state:

    scheduler_thread = threading.Thread(

        target=background_scheduler.start_scheduler,

        daemon=True
    )

    scheduler_thread.start()

    st.session_state.scheduler_started = True
# =========================
# SESSION STATE
# =========================

if "sheet_url" not in st.session_state:

    st.session_state.sheet_url = ""

# =========================
# SIDEBAR
# =========================

st.sidebar.title(
    "Previous Campaigns"
)

st.sidebar.markdown(
    "Click any previous campaign to reload it."
)

# =========================
# LOAD CAMPAIGN HISTORY
# =========================

campaign_file = "campaign_history.json"

try:

    with open(
        campaign_file,
        "r"
    ) as file:

        previous_campaigns = json.load(file)

except:

    previous_campaigns = []

# =========================
# SHOW PREVIOUS CAMPAIGNS
# =========================

for index, campaign in enumerate(
    previous_campaigns
):

    if st.sidebar.button(

        f"Campaign {index + 1}"
    ):

        st.session_state.sheet_url = (

            campaign["sheet_url"]
        )

# =========================
# GOOGLE SHEET INPUT
# =========================

sheet_url = st.text_input(

    "Paste Google Sheet URL",

    value=st.session_state.sheet_url
)

# =========================
# DATAFRAME
# =========================

df = pd.DataFrame()

# =========================
# LOAD SHEET
# =========================

if sheet_url:

    try:

        df = get_google_sheet_data(
            sheet_url
        )

        st.success(
            "Google Sheet Connected"
        )

        # =========================
        # SAVE CURRENT SHEET
        # =========================

        st.session_state.sheet_url = (
            sheet_url
        )

    except Exception as e:

        st.exception(e)

# =========================
# SAVE CAMPAIGN HISTORY
# =========================

existing_urls = [

    c["sheet_url"]

    for c in previous_campaigns
]

if sheet_url and sheet_url not in existing_urls:

    previous_campaigns.append({

        "sheet_url": sheet_url,

        "added_on": str(
            datetime.now()
        )
    })

    with open(
        campaign_file,
        "w"
    ) as file:

        json.dump(

            previous_campaigns,

            file,

            indent=4
        )

# =========================
# REQUIRED COLUMNS
# =========================

if not df.empty:

    required_columns = [

        "name",
        "company",
        "email",
        "domain",
        "status"
    ]

    missing = [

        col for col in required_columns

        if col not in df.columns
    ]

    if missing:

        st.error(
            f"Missing Columns: {missing}"
        )

        st.stop()

# =========================
# DISPLAY DATA
# =========================

if not df.empty:

    st.subheader(
        "Lead Data"
    )

    st.dataframe(

        df,

        width="stretch"
    )

    # =========================
    # METRICS
    # =========================

    total_leads = len(df)

    pending = len(

        df[
            df["status"] == "pending"
        ]
    )

    sent = len(

        df[
            df["status"] == "sent"
        ]
    )

    followups = 0

    if "followup_sent" in df.columns:

        followups = len(

            df[
                df["followup_sent"]
                .astype(str)
                .str.lower() == "yes"
            ]
        )

    col1, col2, col3, col4 = st.columns(4)

    with col1:

        st.metric(

            "Total Leads",

            total_leads
        )

    with col2:

        st.metric(

            "Pending Emails",

            pending
        )

    with col3:

        st.metric(

            "Sent Emails",

            sent
        )

    with col4:

        st.metric(

            "Follow-Ups Sent",

            followups
        )

    # =========================
    # STATUS CHART
    # =========================

    st.subheader(
        "Email Status Distribution"
    )

    status_counts = (

        df["status"]

        .value_counts()
    )

    st.bar_chart(
        status_counts
    )

    # =========================
    # EMAIL TRACKING
    # =========================

    st.subheader(
        "Email Tracking"
    )

    tracking_columns = [

        "name",
        "company",
        "email",
        "status",
        "sent_time",
        "followup_sent",
        "reply_status"
    ]

    available_cols = [

        col

        for col in tracking_columns

        if col in df.columns
    ]

    st.dataframe(

        df[available_cols],

        width="stretch"
    )

    # =========================
    # SAVE SHEET URL
    # =========================

    with open(
        "sheet_url.txt",
        "w"
    ) as file:

        file.write(
            sheet_url
        )

    # =========================
    # ACTION BUTTONS
    # =========================

    col1, col2 = st.columns(2)

    # =========================
    # SEND EMAILS
    # =========================

    with col1:

        if st.button(
            "Send Pending Emails"
        ):

            try:

                run_email_campaign()

                st.success(
                    "Emails Sent Successfully"
                )

                st.rerun()

            except Exception as e:

                st.exception(e)

    # =========================
    # FOLLOWUPS
    # =========================

    with col2:

        if st.button(
            "Run Follow-Ups"
        ):

            try:

                run_followups()

                st.success(
                    "Follow-Ups Sent"
                )

                st.rerun()

            except Exception as e:

                st.exception(e)

    # =========================
    # SCHEDULE EMAILS
    # =========================

    st.subheader(
        "Schedule Emails"
    )

    with st.expander(
        "Open Scheduler"
    ):

        schedule_date = st.date_input(
            "Select Date"
        )

        schedule_hour = st.selectbox(

            "Hour",

            list(range(24))
        )

        schedule_minute = st.selectbox(

            "Minute",

            [
                "00",
                "05",
                "10",
                "15",
                "20",
                "25",
                "30",
                "35",
                "40",
                "45",
                "50",
                "55"
            ]
        )

        schedule_time = time(

            schedule_hour,

            int(schedule_minute)
        )

        if st.button(
            "Schedule Emails"
        ):

            scheduled_datetime = (

                datetime.combine(

                    schedule_date,

                    schedule_time
                )
            )

            try:

                with open(
                    "scheduled_jobs.json",
                    "r"
                ) as file:

                    jobs = json.load(file)

            except:

                jobs = []

            jobs.append({

                "sheet_url": sheet_url,

                "schedule_time": scheduled_datetime.strftime(

                    "%Y-%m-%d %H:%M:%S"
                ),

                "status": "pending"
            })

            with open(
                "scheduled_jobs.json",
                "w"
            ) as file:

                json.dump(

                    jobs,

                    file,

                    indent=4
                )

            st.success(
                "Emails Scheduled Successfully"
            )

    # =========================
    # SHOW SCHEDULED JOBS
    # =========================

    st.subheader(
        "Scheduled Jobs"
    )

    try:

        with open(
            "scheduled_jobs.json",
            "r"
        ) as file:

            jobs = json.load(file)

        if jobs:

            jobs_df = pd.DataFrame(
                jobs
            )

            st.dataframe(

                jobs_df,

                width="stretch"
            )

        else:

            st.info(
                "No Scheduled Jobs"
            )

    except:

        st.info(
            "No Scheduled Jobs"
        )