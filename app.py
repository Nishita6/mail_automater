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

def run_email_campaign_automated(creds, url):
    """
    A thread-safe version of the campaign runner.
    """
    from modules.gmail_sender import send_email
    from modules.google_sheets import get_google_sheet_data, update_sheet_status, update_sent_time
    from modules.resume_selector import select_resume

    # Load template
    with open("templates/template.txt", "r", encoding="utf-8") as file:
        template = file.read()

    # Get data using the URL passed from the job
    df = get_google_sheet_data(url)
    pending_leads = df[df["status"] == "pending"]

    for index, row in pending_leads.iterrows():
        body = template.format(
            name=row["name"],
            company=row["company"],
            domain=row["domain"]
        )
        resume_path = select_resume(row["domain"])

        try:
            send_email(
                creds["EMAIL"],
                creds["APP_PASSWORD"],
                row["email"],
                "Application for Internship | IIT Kharagpur",
                body,
                resume_path
            )
            update_sheet_status(url, row["email"], "sent")
            update_sent_time(url, row["email"])
        except Exception as e:
            print(f"Error sending to {row['email']}: {e}")


def run_email_campaign():
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