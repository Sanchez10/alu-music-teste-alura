import os
from flask import current_app

def enviar_email(destinatario, assunto, corpo):
    if current_app.config.get("TESTING") or os.getenv("MOCK_EMAIL") == "1":
        print(f"[MOCK EMAIL] Para: {destinatario} | Assunto: {assunto}\n{corpo}")
    else:
        import smtplib
        from email.mime.text import MIMEText

        msg = MIMEText(corpo)
        msg["Subject"] = assunto
        msg["From"] = os.getenv("EMAIL_FROM")
        msg["To"] = destinatario

        with smtplib.SMTP(os.getenv("SMTP_HOST"), int(os.getenv("SMTP_PORT"))) as server:
            server.starttls()
            server.login(os.getenv("SMTP_USER"), os.getenv("SMTP_PASS"))
            server.send_message(msg)
