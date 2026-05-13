
from modules.google_sheets import (
    get_google_sheet_data
)

df = get_google_sheet_data("https://docs.google.com/spreadsheets/d/1aCJ2Kw5PkIAHwiCUI0X-KZccdKg1n0qsmwkh8RdMxPM/edit?usp=sharing")

print(df)