from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from utils.smtp_process.celery_server import make_celery
from celery import shared_task
import smtplib

celery = make_celery()


# @celery.task(name=__name__)
@shared_task
def mailing(mail, password, to_address: str, reminder: str):
    """
    Run mailing function
    """
    with smtplib.SMTP(host='smtp.yandex.ru') as smtp:
        msg = MIMEMultipart()
        msg['Subject'] = 'Reminder'
        msg['From'] = mail
        msg['TO'] = to_address

        text = f"Hi!\nReminder for you!\n{reminder}"
        part_1 = MIMEText(text, 'plain')
        msg.attach(part_1)

        smtp.starttls()
        smtp.login(user=mail, password=password)
        smtp.sendmail(from_addr=mail, to_addrs=to_address, msg=msg.as_string())
