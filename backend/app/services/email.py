import smtplib
from email.message import EmailMessage
from app.core.config import settings

def send_email(subject: str, to: str, body: str):
    msg = EmailMessage()
    msg["Subject"] = subject
    msg["From"] = settings.EMAILS_FROM_EMAIL
    msg["To"] = to
    msg.set_content(body)

    try:
        with smtplib.SMTP(settings.SMTP_HOST, settings.SMTP_PORT) as server:
            if settings.SMTP_USER and settings.SMTP_PASSWORD:
                server.login(settings.SMTP_USER, settings.SMTP_PASSWORD)
            server.send_message(msg)
        return True
    except Exception as e:
        print(f"Failed to send email: {e}")
        return False
