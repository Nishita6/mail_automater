import base64
import os

from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email import encoders

from googleapiclient.errors import HttpError


def create_message(sender, to, subject, body, attachment_path):

    message = MIMEMultipart()

    message['to'] = to
    message['from'] = sender
    message['subject'] = subject

    # Email body
    message.attach(MIMEText(body, 'html'))

    # Attachment
    filename = os.path.basename(attachment_path)

    with open(attachment_path, 'rb') as attachment:

        part = MIMEBase('application', 'octet-stream')

        part.set_payload(attachment.read())

    encoders.encode_base64(part)

    part.add_header(
        'Content-Disposition',
        f'attachment; filename={filename}'
    )

    message.attach(part)

    raw_message = base64.urlsafe_b64encode(
        message.as_bytes()
    ).decode()

    return {
        'raw': raw_message
    }


def send_email(
    service,
    sender,
    to,
    subject,
    body,
    attachment_path
):

    try:

        message = create_message(
            sender,
            to,
            subject,
            body,
            attachment_path
        )

        sent_message = service.users().messages().send(
            userId='me',
            body=message
        ).execute()

        print(f"Email sent to {to}")

        return sent_message

    except HttpError as error:

        print(f"An error occurred: {error}")

        return None