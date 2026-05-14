import streamlit as st

from modules.gmail_sender import (
    send_email
)

from modules.resume_selector import (
    select_resume
)

from modules.google_sheets import (

    get_google_sheet_data,

    update_sheet_status,

    update_sent_time
)

# =========================
# EMAIL CONFIG
# =========================

SENDER_EMAIL = st.secrets["EMAIL"]

APP_PASSWORD = st.secrets["APP_PASSWORD"]

# =========================
# SUBJECT
# =========================

SUBJECT = (
    "Application for Internship | IIT Kharagpur"
)

# =========================
# LOAD TEMPLATE
# =========================

with open(

    "templates/template.txt",

    "r",

    encoding="utf-8"

) as file:

    template = file.read()

# =========================
# LOAD SHEET URL
# =========================

with open(
    "sheet_url.txt",
    "r"
) as file:

    sheet_url = file.read()

# =========================
# LOAD GOOGLE SHEET
# =========================

df = get_google_sheet_data(
    sheet_url
)

# =========================
# FILTER PENDING LEADS
# =========================

pending_leads = df[
    df["status"] == "pending"
]

# =========================
# SEND EMAILS
# =========================

for index, row in pending_leads.iterrows():

    name = row["name"]

    company = row["company"]

    email = row["email"]

    domain = row["domain"]

    body = template.format(

        name=name,

        company=company,

        domain=domain
    )

    # Select Resume
    resume_path = select_resume(
        domain
    )

    try:

        print(f"Sending to {email}")

        send_email(

            SENDER_EMAIL,

            APP_PASSWORD,

            email,

            SUBJECT,

            body,

            resume_path
        )

        print(f"SUCCESS: {email}")

        # Update Sheet Status
        update_sheet_status(

            sheet_url,

            email,

            "sent"
        )

        # Update Sent Time
        update_sent_time(

            sheet_url,

            email
        )

    except Exception as e:

        print(
            f"FAILED: {email}"
        )

        print(e)