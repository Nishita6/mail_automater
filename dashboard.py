import streamlit as st
import pandas as pd
import json
from datetime import datetime, time

from app import run_email_campaign
from followup_scheduler import run_followups

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
# GOOGLE SHEET INPUT
# =========================

sheet_url = st.text_input(
    "Paste Google Sheet URL"
)

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

    except Exception as e:

        st.exception(e)

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
        df[df["status"] == "pending"]
    )

    sent = len(
        df[df["status"] == "sent"]
    )

    col1, col2, col3 = st.columns(3)

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

            scheduled_datetime = datetime.combine(

                schedule_date,

                schedule_time
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
    # SHOW JOBS
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