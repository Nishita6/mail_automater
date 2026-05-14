


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

import streamlit as st
# =========================
# AUTHENTICATE GMAIL
# =========================



# =========================
# SENDER EMAIL
# =========================



SENDER_EMAIL = (
    "gnishita16@gmail.com"
)

SENDER_EMAIL = st.secrets[SENDER_EMAIL]

APP_PASSWORD = st.secrets["qfzj utia vzfz pdtj"
]
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
# LOAD SHEET DATA
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

        send_email(
            service,
            SENDER_EMAIL,
            email,
            SUBJECT,
            body,
            resume_path
        )

        # Update Status
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

        print(
            f"Email sent to {email}"
        )

    except Exception as e:

        print(
            f"Failed for {email}"
        )

        print(e)