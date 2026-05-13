import sqlite3

# Connect database
conn = sqlite3.connect(
    "database/outreach.db"
)

cursor = conn.cursor()

# Create table
cursor.execute("""

CREATE TABLE IF NOT EXISTS leads (

    id INTEGER PRIMARY KEY AUTOINCREMENT,

    name TEXT,

    company TEXT,

    email TEXT UNIQUE,

    domain TEXT,

    status TEXT,

    sent_time TEXT,

    followup_time TEXT,

    reply_status TEXT,

    followup_sent INTEGER

)

""")

conn.commit()

conn.close()

print(
    "Database Created Successfully"
)