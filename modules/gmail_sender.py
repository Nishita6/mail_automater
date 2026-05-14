import smtplib

from email.mime.text import MIMEText

from email.mime.multipart import MIMEMultipart

from email.mime.base import MIMEBase

from email import encoders


def send_email(

    sender_email,

    app_password,

    receiver_email,

    subject,

    body,

    attachment_path=None
):

    msg = MIMEMultipart()

    msg["From"] = sender_email

    msg["To"] = receiver_email

    msg["Subject"] = subject

    msg.attach(
        MIMEText(body, "plain")
    )

    # =========================
    # ATTACH RESUME
    # =========================

    if attachment_path:

        with open(
            attachment_path,
            "rb"
        ) as attachment:

            part = MIMEBase(
                "application",
                "octet-stream"
            )

            part.set_payload(
                attachment.read()
            )

        encoders.encode_base64(part)

        part.add_header(

            "Content-Disposition",

            f"attachment; filename={attachment_path}"
        )

        msg.attach(part)

    # =========================
    # SMTP SERVER
    # =========================

    server = smtplib.SMTP(
        "smtp.gmail.com",
        587
    )

    server.starttls()

    server.login(
        sender_email,
        app_password
    )

    server.sendmail(

        sender_email,

        receiver_email,

        msg.as_string()
    )

    server.quit()