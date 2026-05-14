import os
import streamlit as st
from modules.gmail_sender import send_email
from modules.resume_selector import select_resume
from modules.google_sheets import get_google_sheet_data, update_sheet_status, update_sent_time

# =========================
# EMAIL CONFIG
# =========================
SENDER_EMAIL = st.secrets["EMAIL"]
APP_PASSWORD = st.secrets["APP_PASSWORD"]
SUBJECT = "Application for Internship | IIT Kharagpur"

# =====================================================================
# FUNCTION 1: AUTOMATED BACKGROUND ENGINE
# =====================================================================
def run_email_campaign_automated(creds, url):
    """
    A thread-safe version of the campaign runner.
    """
    base_path = os.path.dirname(os.path.abspath(__file__))
    template_path = os.path.join(base_path, "templates", "template.txt")

    try:
        with open(template_path, "r", encoding="utf-8") as file:
            template_content = file.read()
    except Exception as e:
        print(f"❌ Error loading template: {e}")
        return

    df = get_google_sheet_data(url)
    pending_leads = df[df["status"] == "pending"]

    for index, row in pending_leads.iterrows():
        email = str(row.get("email", "")).strip()
        company = str(row.get("company", "the company")).strip()
        domain = str(row.get("domain", "General")).strip()

        if not email:
            continue

        # FIX: Explicit string replacement prevents structural KeyError drops
        email_body = template_content.replace("{company}", company)

        resume_path = select_resume(domain)

        try:
            send_email(
                creds["EMAIL"],
                creds["APP_PASSWORD"],
                email,
                SUBJECT,
                email_body,
                resume_path
            )
            update_sheet_status(url, email, "sent")
            update_sent_time(url, email)
            print(f"✅ Successfully sent to {email}")
        except Exception as e:
            print(f"❌ Error sending to {email}: {e}")


# =====================================================================
# FUNCTION 2: MANUAL UI CLICK RUNNER
# =====================================================================
def run_email_campaign():
    base_path = os.path.dirname(os.path.abspath(__file__))
    template_path = os.path.join(base_path, "templates", "template.txt")

    with open(template_path, "r", encoding="utf-8") as file:
        template = file.read()

    # Read tracking sheet path safely
    sheet_url_path = os.path.join(base_path, "sheet_url.txt")
    with open(sheet_url_path, "r") as file:
        sheet_url = file.read().strip()

    df = get_google_sheet_data(sheet_url)
    pending_leads = df[df["status"] == "pending"]

    for index, row in pending_leads.iterrows():
        name = row["name"]
        company = row["company"]
        email = row["email"]
        domain = row["domain"]

        # FIX: Use explicit replace loop to protect clean HTML rendering
        body = template.replace("{company}", company)

        resume_path = select_resume(domain)

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

            update_sheet_status(sheet_url, email, "sent")
            update_sent_time(sheet_url, email)

        except Exception as e:
            print(f"FAILED: {email}")
            print(e)
