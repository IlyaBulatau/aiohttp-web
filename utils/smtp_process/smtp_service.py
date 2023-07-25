import aiosmtplib
from aiohttp import web
from database.models import Reminder

from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

class Mailinger:

    def __init__(self, app: web.Application, to_address: str, reminder: Reminder):
        self._app: web.Application = app
        self._mail: str = self._app['config']['app_mail']
        self._password: str = self._app['config']['app_mail_password']
        self.to_address: str = to_address
        self.content: str = reminder.content
        
    @property
    def app(self):
        return self._app
    
    @property
    def mail(self):
        return self._mail
    
    @property
    def password(self):
        return self._password

    async def send_email(self):
        msg = self.create_message()

        async with aiosmtplib.SMTP(hostname='smtp.yandex.ru', password=587, timeout=15) as smtp:
            await smtp.login(self.mail, password=self.password)
            await smtp.sendmail(sender=self.mail, recipients=[self.to_address], message=msg.as_string())
    
    def create_message(self):
        msg = MIMEMultipart()
        msg['Subject'] = 'Reminder'
        msg['From'] = self.mail
        msg['To'] = self.to_address

        self.text_for_message(msg)

        return msg

    def text_for_message(self, msg):
        text = f"Hi!\nReminder for you!\n{self.content}"
        part_1 = MIMEText(text, 'plain')
        msg.attach(part_1)
