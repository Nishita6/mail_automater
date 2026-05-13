from datetime import datetime

from modules.db_manager import (
    get_connection
)

# Add lead
def add_lead(
    name,
    company,
    email,
    domain
):

    conn = get_connection()

    cursor = conn.cursor()

    try:

        cursor.execute("""

        INSERT INTO leads (

            name,
            company,
            email,
            domain,
            status,
            sent_time,
            followup_time,
            reply_status,
            followup_sent

        )

        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)

        """, (

            name,
            company,
            email,
            domain,

            "pending",

            "",

            "",

            "no_reply",

            0
        ))

        conn.commit()

        print(
            f"Lead Added: {email}"
        )

    except Exception as e:

        print(
            f"Lead Exists: {email}"
        )

    conn.close()


# Check existing lead
def lead_exists(email):

    conn = get_connection()

    cursor = conn.cursor()

    cursor.execute("""

    SELECT *

    FROM leads

    WHERE email = ?

    """, (email,))

    result = cursor.fetchone()

    conn.close()

    return result is not None


# Mark initial email sent
def mark_email_sent(email):

    conn = get_connection()

    cursor = conn.cursor()

    current_time = datetime.now().strftime(
        "%Y-%m-%d %H:%M:%S"
    )

    cursor.execute("""

    UPDATE leads

    SET
        status = ?,
        sent_time = ?

    WHERE email = ?

    """, (

        "sent",
        current_time,
        email

    ))

    conn.commit()

    conn.close()

    print(
        f"Updated Status: {email}"
    )


# Get follow-up candidates
def get_followup_candidates():

    conn = get_connection()

    cursor = conn.cursor()

    cursor.execute("""

    SELECT *

    FROM leads

    WHERE
        status = 'sent'

    AND
        followup_sent = 0

    """)

    results = cursor.fetchall()

    conn.close()

    return results


# Mark follow-up sent
def mark_followup_sent(email):

    conn = get_connection()

    cursor = conn.cursor()

    current_time = datetime.now().strftime(
        "%Y-%m-%d %H:%M:%S"
    )

    cursor.execute("""

    UPDATE leads

    SET
        followup_sent = ?,
        followup_time = ?

    WHERE email = ?

    """, (

        1,
        current_time,
        email

    ))

    conn.commit()

    conn.close()

    print(
        f"Follow-up Updated: {email}"
    )