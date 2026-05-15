import gspread
import pandas as pd
from datetime import datetime
import streamlit as st
from oauth2client.service_account import ServiceAccountCredentials

# =========================
# GOOGLE API SCOPE
# =========================
scope = [
    "https://spreadsheets.google.com/feeds",
    "https://www.googleapis.com/auth/drive"
]

# =========================
# AUTH (cached)
# =========================
@st.cache_resource
def get_client():
    creds_dict = dict(st.secrets["gcp_service_account"])

    creds = ServiceAccountCredentials.from_json_keyfile_dict(
        creds_dict,
        scope
    )

    return gspread.authorize(creds)


client = get_client()


# =========================
# HELPERS
# =========================
def extract_sheet_id(url):
    return url.split("/d/")[1].split("/")[0]


@st.cache_resource
def get_sheet(sheet_url):
    sheet_id = extract_sheet_id(sheet_url)
    return client.open_by_key(sheet_id).sheet1


# =========================
# READ DATA (cached)
# =========================
@st.cache_data(ttl=120)
def get_google_sheet_data(sheet_url):
    sheet = get_sheet(sheet_url)

    records = sheet.get_all_records()
    return pd.DataFrame(records)


# =========================
# UPDATE STATUS (optimized)
# =========================
def update_sheet_status(sheet_url, email, new_status):
    sheet = get_sheet(sheet_url)

    records = sheet.get_all_values()  # faster than get_all_records

    for i, row in enumerate(records[1:], start=2):  # skip header
        if row[0] == email:  # assuming email is column A
            sheet.update_cell(i, 5, new_status)
            break


# =========================
# UPDATE SENT TIME
# =========================
def update_sent_time(sheet_url, email):
    sheet = get_sheet(sheet_url)

    records = sheet.get_all_values()

    current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    for i, row in enumerate(records[1:], start=2):
        if row[0] == email:
            sheet.update_cell(i, 6, current_time)
            break


# =========================
# UPDATE FOLLOWUP STATUS
# =========================
def update_followup_status(sheet_url, email):
    sheet = get_sheet(sheet_url)

    records = sheet.get_all_values()

    for i, row in enumerate(records[1:], start=2):
        if row[0] == email:
            sheet.update_cell(i, 7, "yes")
            break