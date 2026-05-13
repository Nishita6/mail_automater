import pandas as pd

LEADS_FILE = "data/leads.csv"

def load_leads():

    df = pd.read_csv(LEADS_FILE)

    return df

def get_pending_leads():

    df = load_leads()

    pending = df[df['status'] == 'pending']

    return pending

def mark_as_sent(email):

    df = load_leads()

    df.loc[df['email'] == email, 'status'] = 'sent'

    df.to_csv(LEADS_FILE, index=False)