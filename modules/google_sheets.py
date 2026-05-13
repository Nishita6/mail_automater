import gspread

import pandas as pd

from datetime import datetime

from oauth2client.service_account import (
    ServiceAccountCredentials
)

# =========================
# GOOGLE API SCOPE
# =========================

scope = [

    "https://spreadsheets.google.com/feeds",

    "https://www.googleapis.com/auth/drive"
]

# =========================
# AUTHENTICATION
# =========================

creds = (
    ServiceAccountCredentials
    .from_json_keyfile_name(
        "service_account.json",
        scope
    )
)

client = gspread.authorize(
    creds
)

# =========================
# LOAD SHEET DATA
# =========================

def get_google_sheet_data(sheet_url):

    sheet = client.open_by_url(
        sheet_url
    ).sheet1

    records = sheet.get_all_records()

    df = pd.DataFrame(records)

    return df

# =========================
# UPDATE STATUS
# =========================

def update_sheet_status(

    sheet_url,

    email,

    new_status
):

    sheet = client.open_by_url(
        sheet_url
    ).sheet1

    records = sheet.get_all_records()

    for index, row in enumerate(records):

        if row["email"] == email:

            # Column 5 = status
            sheet.update_cell(

                index + 2,

                5,

                new_status
            )

            print(
                f"{email} updated to {new_status}"
            )

            break

# =========================
# UPDATE SENT TIME
# =========================

def update_sent_time(

    sheet_url,

    email
):

    sheet = client.open_by_url(
        sheet_url
    ).sheet1

    records = sheet.get_all_records()

    current_time = datetime.now().strftime(

        "%Y-%m-%d %H:%M:%S"
    )

    for index, row in enumerate(records):

        if row["email"] == email:

            # Column 6 = sent_time
            sheet.update_cell(

                index + 2,

                6,

                current_time
            )

            break

# =========================
# UPDATE FOLLOWUP STATUS
# =========================

def update_followup_status(

    sheet_url,

    email
):

    sheet = client.open_by_url(
        sheet_url
    ).sheet1

    records = sheet.get_all_records()

    for index, row in enumerate(records):

        if row["email"] == email:

            # Column 7 = followup_sent
            sheet.update_cell(

                index + 2,

                7,

                "yes"
            )

            break