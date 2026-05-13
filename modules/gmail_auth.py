import os.path

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build

SCOPES = [
    "https://www.googleapis.com/auth/gmail.send"
]


def authenticate_gmail():

    creds = None

    # Load saved token
    if os.path.exists("token.json"):

        creds = Credentials.from_authorized_user_file(
            "token.json",
            SCOPES
        )

    # If credentials invalid
    if not creds or not creds.valid:

        # Refresh token
        if creds and creds.expired and creds.refresh_token:

            creds.refresh(Request())

        else:

            flow = InstalledAppFlow.from_client_secrets_file(
                "credentials.json",
                SCOPES
            )

            creds = flow.run_local_server(port=0)

        # Save token
        with open("token.json", "w") as token:

            token.write(creds.to_json())

    # Build Gmail service
    service = build(
        "gmail",
        "v1",
        credentials=creds,
        cache_discovery=False
    )

    return service