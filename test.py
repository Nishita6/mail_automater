from modules.gmail_auth import authenticate_gmail

service = authenticate_gmail()

results = service.users().labels().list(
    userId='me'
).execute()

print(results)