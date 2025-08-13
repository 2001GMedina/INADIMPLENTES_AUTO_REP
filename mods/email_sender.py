# mods/email_sender.py
import os
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.image import MIMEImage

def send_email(subject: str, html_content: str, logo_path="utils/logo.png"):
    # Variáveis do .env
    EMAIL_USER = os.getenv("EMAIL_USER")
    EMAIL_PASS = os.getenv("EMAIL_PASS")
    EMAIL_HOST = os.getenv("EMAIL_HOST")
    EMAIL_PORT = int(os.getenv("EMAIL_PORT"))
    EMAIL_TO = os.getenv("EMAIL_TO").split(",")  # lista de destinatários

    # Criar mensagem
    msg = MIMEMultipart()
    msg['From'] = EMAIL_USER
    msg['To'] = ", ".join(EMAIL_TO)
    msg['Subject'] = subject

    # Adicionar corpo HTML
    msg.attach(MIMEText(html_content, 'html'))

    # Anexar logo como MIMEImage com Content-ID
    if os.path.exists(logo_path):
        with open(logo_path, "rb") as f:
            logo_data = f.read()
        logo = MIMEImage(logo_data)
        logo.add_header('Content-ID', '<logo>')  # Referência no HTML como cid:logo
        logo.add_header('Content-Disposition', 'inline', filename=os.path.basename(logo_path))
        msg.attach(logo)

    # Enviar e-mail via SMTP SSL
    with smtplib.SMTP_SSL(EMAIL_HOST, EMAIL_PORT) as server:
        server.login(EMAIL_USER, EMAIL_PASS)
        server.send_message(msg)

    print(f"E-mail enviado com sucesso para: {', '.join(EMAIL_TO)}")
