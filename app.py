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

import os

def run_email_campaign_automated(creds, url):
    """
    A thread-safe version of the campaign runner.
    """
    from modules.gmail_sender import send_email
    from modules.google_sheets import get_google_sheet_data, update_sheet_status, update_sent_time
    from modules.resume_selector import select_resume

    # 1. Use an Absolute Path for the template
    base_path = os.path.dirname(__file__)
    template_path = os.path.join(base_path, "templates", "template.txt")

    try:
        with open(template_path, "r", encoding="utf-8") as file:
            template_content = file.read()
    except Exception as e:
        print(f"❌ Error loading template: {e}")
        return # Stop if template can't be read

    # 2. Get data
    df = get_google_sheet_data(url)
    pending_leads = df[df["status"] == "pending"]

    for index, row in pending_leads.iterrows():
        # 3. Carefully format the body
        try:
            email_body = template_content.format(
                name=row.get("name", "Candidate"),
                company=row.get("company", "the company"),
                domain=row.get("domain", "your team")
            )
        except KeyError as e:
            print(f"❌ Formatting error: Missing column {e} in Google Sheet")
            continue

        resume_path = select_resume(row["domain"])

        try:
            # 4. Verify send_email is receiving email_body
            send_email(
                creds["EMAIL"],
                creds["APP_PASSWORD"],
                row["email"],
                "Application for Internship | IIT Kharagpur",
                email_body, # Ensure this variable is NOT empty
                resume_path
            )
            update_sheet_status(url, row["email"], "sent")
            update_sent_time(url, row["email"])
            print(f"✅ Successfully sent to {row['email']}")
        except Exception as e:
            print(f"❌ Error sending to {row['email']}: {e}")

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