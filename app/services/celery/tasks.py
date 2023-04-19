from .celery import celery
import smtplib, ssl
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.application import MIMEApplication
from app.config import cfg


def attach_file_to_email(message, file):
    # 'image.png', ('chart.png', {'Content-ID': '<myimageid>'},)
    if isinstance(file, tuple):
        file_name, ext_headers = file
    else:
        file_name, ext_headers = (file, None,)

    with open(file_name, 'rb') as f:
        file_attachment = MIMEApplication(f.read())
   
    file_attachment.add_header('Content-Disposition', f'attachment; filename= {file_name}')

    if ext_headers is not None:
        for name, value in ext_headers.items():
            file_attachment.add_header(name, value)
    message.attach(file_attachment)



@celery.task
def send_email(email_data):
    email_sender = email_data['sender']
    email_password = ''
    email_receiver = email_data['to']

    # Set the subject and body of the email
    subject = email_data['subject']
    html = email_data['html']

    email_message = MIMEMultipart()
    email_message['From'] = email_sender
    email_message['To'] = email_receiver
    email_message['Subject'] = subject

    email_message.attach(MIMEText(html, "html"))

    if cfg.mail_server == 'localhost' and cfg.mail_port == 1025:
        email_string = email_message.as_string()

        server = smtplib.SMTP(cfg.mail_server, cfg.mail_port)
        server.sendmail(email_sender, email_receiver, email_string)
        server.quit()

    if cfg.mail_use_ssl and cfg.mail_port == 465:
        files = email_data.get('files', [])
        for file in files:
            attach_file_to_email(email_message, file)
        email_string = email_message.as_string()
        context = ssl.create_default_context()
        with smtplib.SMTP_SSL(cfg.mail_server, cfg.mail_port, context=context) as server:
            server.login(cfg.mail_username, cfg.mail_password)
            server.sendmail(email_sender, email_receiver, email_string)

    if cfg.mail_use_tls and cfg.mail_port == 587:
        files = email_data.get('files', [])
        for file in files:
            attach_file_to_email(email_message, file)
        email_string = email_message.as_string()
        context = ssl.create_default_context()
        with smtplib.SMTP(cfg.mail_server, cfg.mail_port) as server:
            server.ehlo()
            server.starttls(context=context)
            server.ehlo()
            server.login(cfg.mail_username, cfg.mail_password)
            server.sendmail(email_sender, email_receiver, email_string)
