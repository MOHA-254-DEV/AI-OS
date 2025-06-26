import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from typing import Optional

from app.core.config import settings

def send_email(
    to_email: str,
    subject: str,
    body: str,
    html: Optional[str] = None,
    from_email: Optional[str] = None,
    from_name: Optional[str] = None,
):
    if not settings.EMAILS_ENABLED:
        return False

    msg = MIMEMultipart("alternative")
    msg["Subject"] = subject
    msg["From"] = f"{from_name or settings.EMAILS_FROM_NAME} <{from_email or settings.EMAILS_FROM_EMAIL}>"
    msg["To"] = to_email

    part1 = MIMEText(body, "plain")
    msg.attach(part1)
    if html:
        part2 = MIMEText(html, "html")
        msg.attach(part2)

    try:
        with smtplib.SMTP(settings.SMTP_HOST, settings.SMTP_PORT) as server:
            server.starttls()
            server.login(settings.SMTP_USER, settings.SMTP_PASSWORD)
            server.sendmail(
                settings.EMAILS_FROM_EMAIL,
                to_email,
                msg.as_string(),
            )
        return True
    except Exception as e:
        print(f"Email sending failed: {e}")
        return False
