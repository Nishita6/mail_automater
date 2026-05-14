from datetime import datetime
import streamlit as st

from modules.gmail_sender import (
    send_email
)

from modules.google_sheets import (

    get_google_sheet_data,

    update_followup_status
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
    "Following up regarding internship opportunity"
)

# =========================
# MAIN FUNCTION
# =========================

def run_followups():

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
    # LOAD TEMPLATE
    # =========================

    with open(
        "templates/followup.txt",
        "r",
        encoding="utf-8"
    ) as file:

        template = file.read()

    # =========================
    # FOLLOWUP LOGIC
    # =========================

    for index, row in df.iterrows():

        try:

            # =========================
            # SKIP INVALID ROWS
            # =========================

            if (

                row["status"] != "sent"

                or

                str(
                    row.get(
                        "followup_sent",
                        ""
                    )
                ).lower() == "yes"

                or

                str(
                    row.get(
                        "reply_status",
                        ""
                    )
                ).lower() == "replied"
            ):

                continue

            # =========================
            # SENT TIME
            # =========================

            sent_time = datetime.strptime(

                str(row["sent_time"]),

                "%Y-%m-%d %H:%M:%S"
            )

            days_passed = (
                datetime.now() - sent_time
            ).days

            # =========================
            # SEND FOLLOWUP AFTER 2 DAYS
            # =========================

            if days_passed >= 2:

                body = template.format(

                    name=row["name"],

                    company=row["company"]
                )

                print(
                    f"Sending follow-up to {row['email']}"
                )

                send_email(

                    SENDER_EMAIL,

                    APP_PASSWORD,

                    row["email"],

                    SUBJECT,

                    body,

                    None
                )

                # =========================
                # UPDATE SHEET
                # =========================

                update_followup_status(

                    sheet_url,

                    row["email"]
                )

                print(
                    f"Follow-up sent to {row['email']}"
                )

        except Exception as e:

            print(
                f"Failed for {row['email']}"
            )

            print(e)

# =========================
# RUN SCRIPT
# =========================

if __name__ == "__main__":

    run_followups()