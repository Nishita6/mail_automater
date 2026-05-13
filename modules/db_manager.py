import sqlite3

DATABASE_PATH = "database/outreach.db"

def get_connection():

    conn = sqlite3.connect(DATABASE_PATH)

    return conn