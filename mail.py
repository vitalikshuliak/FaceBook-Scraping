import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from utils import get_env_value
from dotenv import load_dotenv
from pathlib import Path

ENV_PATH = Path(__file__).resolve().parent/ ".env"
load_dotenv(dotenv_path=ENV_PATH)

def send_join_request_email(group_url):
    # set up the SMTP server
    smtp_server = "smtp.gmail.com"
    smtp_port = 587  
    smtp_username = get_env_value("SMTP_USERNAME")
    smtp_password = get_env_value("SMTP_PASSWORD")
    smtp_conn = smtplib.SMTP(smtp_server, smtp_port)
    smtp_conn.starttls()
    smtp_conn.login(smtp_username, smtp_password)

    # create the email message
    sender_email = get_env_value("SENDER_EMAIL")
    receiver_email = get_env_value("RECEIVER_EMAIL")
    subject = "Private Facebook Group Join Request"
    body = f'''\
Hi Admin,

A new user has requested to join the private Facebook group and needs to answer the group questions. Please check the following group URL:
{group_url}

Thanks,
Savage Sales
'''.format(group_url)
    message = MIMEMultipart()
    message["From"] = sender_email
    message["To"] = receiver_email
    message["Subject"] = subject
    message.attach(MIMEText(body, "plain"))
    message.add_header('reply-to', sender_email)
    # send the email
    try:
        smtp_conn.sendmail(sender_email, receiver_email, message.as_string())
        print("Email sent successfully!")
    except Exception as e:
        print("Error sending email:", e)

    # close the SMTP connection
    smtp_conn.quit()

