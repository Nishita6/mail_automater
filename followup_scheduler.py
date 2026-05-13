from datetime import datetime

from modules.gmail_auth import (
    authenticate_gmail
)

from modules.gmail_sender import (
    send_email
)

from modules.google_sheets import (

    get_google_sheet_data,

    update_followup_status
)

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
# AUTHENTICATE GMAIL
# =========================

service = authenticate_gmail()

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
# SETTINGS
# =========================

SENDER_EMAIL = (
    "gnishita16@gmail.com"
)

SUBJECT = (
    "Following up regarding internship opportunity"
)

# =========================
# FOLLOWUP LOGIC
# =========================

for index, row in df.iterrows():

    try:

        # Skip invalid rows
        if (

            row["status"] != "sent"

            or

            row["followup_sent"] == "yes"

            or

            row["reply_status"] == "replied"
        ):

            continue

        sent_time = datetime.strptime(

            row["sent_time"],

            "%Y-%m-%d %H:%M:%S"
        )

        days_passed = (
            datetime.now() - sent_time
        ).days

        # Send after 3 days
        if days_passed >= 2:

            body = template.format(

                name=row["name"],

                company=row["company"]
            )

            send_email(

                service,

                SENDER_EMAIL,

                row["email"],

                SUBJECT,

                body,

                None
            )

            update_followup_status(

                sheet_url,

                row["email"]
            )

            print(
                f"Follow-up sent to {row['email']}"
            )

    except Exception as e:

        print(e)