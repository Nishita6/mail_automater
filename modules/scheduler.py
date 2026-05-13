import streamlit as st

import pandas as pd

import os

import json

from datetime import datetime

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
# SHEET URL INPUT
# =========================

sheet_url = st.text_input(
    "Paste Google Sheet URL"
)

df = pd.DataFrame()

# =========================
# LOAD GOOGLE SHEET
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
        use_container_width=True
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
    # DIRECT SEND BUTTON
    # =========================

    st.subheader(
        "Send Emails Now"
    )

    if st.button(
        "Send Pending Emails"
    ):

        os.system(
            "python app.py"
        )

        st.success(
            "Emails Sent Successfully"
        )

    # =========================
    # SCHEDULE EMAILS
    # =========================

    st.subheader(
        "Schedule Emails"
    )

    schedule_date = st.date_input(
        "Select Date"
    )

    schedule_time = st.time_input(
        "Select Time"
    )

    if st.button(
        "Schedule Pending Emails"
    ):

        scheduled_datetime = datetime.combine(

            schedule_date,

            schedule_time
        )

        # Load existing jobs
        try:

            with open(
                "scheduled_jobs.json",
                "r"
            ) as file:

                jobs = json.load(file)

        except:

            jobs = []

        # Add new job
        jobs.append({

            "sheet_url": sheet_url,

            "schedule_time": scheduled_datetime.strftime(

                "%Y-%m-%d %H:%M:%S"
            ),

            "status": "pending"
        })

        # Save jobs
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
    # FOLLOW-UP BUTTON
    # =========================

    st.subheader(
        "Follow-Ups"
    )

    if st.button(
        "Run Follow-Ups"
    ):

        os.system(
            "python followup_scheduler.py"
        )

        st.success(
            "Follow-Ups Sent"
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
                use_container_width=True
            )

        else:

            st.info(
                "No Scheduled Jobs"
            )

    except:

        st.info(
            "No Scheduled Jobs"
        )