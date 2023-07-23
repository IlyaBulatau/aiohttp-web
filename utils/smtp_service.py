import smtplib
import aiosmtplib
from email.message import EmailMessage
import asyncio



def mailing_reminder(to_addr, message):
    with smtplib.SMTP(host='smtp.yandex.ru', port=587) as smtp:
        smtp.starttls()
        smtp.login('myemail', password='mepass')
        smtp.sendmail(from_addr='fromemail', to_addrs=[to_addr], msg=message)

mailing_reminder('meemail', 'TEST MAILLING')

async def mailing():
    async with aiosmtplib.SMTP(hostname='smtp.yandex.ru', password=587, timeout=15) as smtp:
        await smtp.ehlo()
        await smtp.login('meemail', password='mepass')
        await smtp.sendmail(sender='fromemail', recipients=['listaddr'], message='ASYNC MESSAGE')

# asyncio.run(mailing())