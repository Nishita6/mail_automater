import os
import streamlit as st


def run_email_campaign_automated(creds, url):
    """
    Thread-safe version of the campaign runner.
    """
    from modules.gmail_sender import send_email
    from modules.google_sheets import get_google_sheet_data, update_sheet_status, update_sent_time
    from modules.resume_selector import select_resume

    # 1. FIXED PATHING TYPO
    base_dir = os.path.dirname(os.path.abspath(__file__))
    template_path = os.path.join(base_dir, "templates", "template.txt")

    try:
        if not os.path.exists(template_path):
            print(f"❌ Error: Template not found at {template_path}")
            return

        with open(template_path, "r", encoding="utf-8") as file:
            template_content = file.read()
    except Exception as e:
        print(f"❌ Error reading template: {e}")
        return

    # 2. Get data
    df = get_google_sheet_data(url)
    pending_leads = df[df["status"] == "pending"]

    for index, row in pending_leads.iterrows():
        # Convert row to dictionary for safer .get() access
        lead = row.to_dict()

        # 3. Format Body
        try:
            email_body = template_content.format(
                name=str(lead.get("name", "Candidate")),
                company=str(lead.get("company", "the company")),
                domain=str(lead.get("domain", "your team"))
            )
        except Exception as e:
            print(f"❌ Formatting error for {lead.get('email')}: {e}")
            continue

        resume_path = select_resume(lead.get("domain", ""))

        try:
            # 4. Send Email
            send_email(
                creds["EMAIL"],
                creds["APP_PASSWORD"],
                lead["email"],
                "Application for Internship | IIT Kharagpur",
                email_body,
                resume_path
            )
            update_sheet_status(url, lead["email"], "sent")
            update_sent_time(url, lead["email"])
            print(f"✅ Successfully sent to {lead['email']}")
        except Exception as e:
            print(f"❌ Error sending to {lead.get('email')}: {e}")


def run_email_campaign():
    """
    Manual version triggered by the button in the UI.
    It simply grabs the credentials and calls the automated version!
    """
    creds = {
        "EMAIL": st.secrets["EMAIL"],
        "APP_PASSWORD": st.secrets["APP_PASSWORD"]
    }

    try:
        with open("sheet_url.txt", "r") as f:
            url = f.read().strip()

        # Run the thread-safe logic directly
        run_email_campaign_automated(creds, url)

    except FileNotFoundError:
        st.error("Sheet URL not found. Please connect your Google Sheet first.")