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

    # =========================
    # CREATE EMAIL
    # =========================

    msg = MIMEMultipart()

    msg["From"] = sender_email

    msg["To"] = receiver_email

    msg["Subject"] = subject

    msg.attach(

        MIMEText(body, "html")
    )

    # =========================
    # ATTACH FILE
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

        encoders.encode_base64(
            part
        )

        filename = attachment_path.split(
            "/"
        )[-1]

        part.add_header(

            "Content-Disposition",

            f"attachment; filename={filename}"
        )

        msg.attach(part)

    # =========================
    # SEND EMAIL
    # =========================

    try:

        print(
            "Connecting to Gmail SMTP..."
        )

        server = smtplib.SMTP(

            "smtp.gmail.com",

            587
        )

        server.starttls()

        print(
            "Logging into Gmail..."
        )

        server.login(

            sender_email,

            app_password
        )

        print(
            f"Sending email to {receiver_email}"
        )

        server.sendmail(

            sender_email,

            receiver_email,

            msg.as_string()
        )

        print(
            f"SUCCESS: {receiver_email}"
        )

        server.quit()

    except Exception as e:

        print(
            "EMAIL ERROR:"
        )

        print(e)

        raise e