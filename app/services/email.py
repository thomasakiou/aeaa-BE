import smtplib
from email.message import EmailMessage
from app.core.config import settings

def send_contact_email(name: str, email: str, subject: str, message: str):
    msg = EmailMessage()
    msg['Subject'] = f"[AEAA Contact] {subject}"
    msg['From'] = settings.SMTP_FROM
    msg['To'] = settings.CONTACT_EMAIL
    msg.add_header('Reply-To', email)
    
    body = f"""New message from the AEAA Conference website:

Name:    {name}
Email:   {email}
Subject: {subject}

Message:
{message}
"""
    msg.set_content(body)
    
    if not settings.SMTP_PASS or settings.SMTP_PASS == "":
        print(f"Mock email sent to {settings.CONTACT_EMAIL}:\n{body}")
        return

    with smtplib.SMTP(settings.SMTP_HOST, settings.SMTP_PORT) as server:
        server.starttls()
        server.login(settings.SMTP_USER, settings.SMTP_PASS)
        server.send_message(msg)
