# mods/email_sender.py
import os
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.image import MIMEImage

def send_email(subject: str, html_content: str, logo_path="utils/logo.png"):
    # --- Variáveis do .env ---
    EMAIL_USER = os.getenv("EMAIL_USER")
    EMAIL_PASS = os.getenv("EMAIL_PASS")
    EMAIL_HOST = os.getenv("EMAIL_HOST")
    EMAIL_PORT = int(os.getenv("EMAIL_PORT"))
    EMAIL_TO = os.getenv("EMAIL_TO").split(",")

    # --- Criar mensagem ---
    msg = MIMEMultipart()
    msg['From'] = EMAIL_USER
    msg['To'] = ", ".join(EMAIL_TO)
    msg['Subject'] = subject

    # --- Anexar logo antes do corpo HTML ---
    base_dir = os.path.dirname(os.path.abspath(__file__))
    logo_abspath = os.path.join(base_dir, "..", logo_path)

    if os.path.exists(logo_abspath):
        with open(logo_abspath, "rb") as f:
            logo_data = f.read()
        logo = MIMEImage(logo_data)
        logo.add_header('Content-ID', '<logo>')  # Referência no HTML como cid:logo
        logo.add_header('Content-Disposition', 'inline', filename=os.path.basename(logo_abspath))
        msg.attach(logo)

    # --- Adicionar corpo HTML ---
    msg.attach(MIMEText(html_content, 'html'))

    # --- Enviar e-mail via SMTP SSL ---
    with smtplib.SMTP_SSL(EMAIL_HOST, EMAIL_PORT) as server:
        server.login(EMAIL_USER, EMAIL_PASS)
        server.send_message(msg)

    print(f"E-mail enviado com sucesso para: {', '.join(EMAIL_TO)}")
