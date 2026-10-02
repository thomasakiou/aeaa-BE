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
    
    if settings.SMTP_PORT == 465:
        server_connection = smtplib.SMTP_SSL(settings.SMTP_HOST, settings.SMTP_PORT)
    else:
        server_connection = smtplib.SMTP(settings.SMTP_HOST, settings.SMTP_PORT)

    with server_connection as server:
        if settings.SMTP_PORT != 465:
            server.starttls()
        if settings.SMTP_PASS:
            server.login(settings.SMTP_USER, settings.SMTP_PASS)
        server.send_message(msg)
