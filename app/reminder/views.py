import aiohttp_jinja2
from aiohttp import web
from aiohttp_security import authorized_userid

from utils import auth_verification, log, ReminderSaveForm
from database.models import Reminder
from datetime import datetime
from database.connect import Database
from app.exeption.values_exeption import ContentLenghtExeption, ContentSpaceExeption, ContentStrExeption, TimePassedExeption, EmptyDataExeption

@aiohttp_jinja2.template('index.html')
@auth_verification
async def index(request: web.Request):
    KEYS = {'text': 'Main Page', 'title': 'Reminder', 'reminder_error': None}

    user_id: int = await authorized_userid(request)
    log.warning(f'User activate login in ID: {user_id}')
    
    method: str = request.method.upper()
    db: Database = request.app['db']

    if method == 'GET':
        return KEYS

    elif method == 'POST':
        responce: dict = await request.post()

        # get data
        content: str = responce.get('reminder')
        date_departure: str = responce.get('calendar')
        time_departure: str = responce.get('time')
        
        # validate dataset
        try:
            ReminderSaveForm(content=content, date_departure=date_departure, time_departure=time_departure)
            datetime_departure = datetime.strptime(date_departure+'/'+time_departure, '%Y-%m-%d/%H:%M')
        except ContentStrExeption:
            KEYS['reminder_error'] = 'You text in reminder is not valid'
            return aiohttp_jinja2.render_template('index.html', request, context=KEYS)
        except ContentLenghtExeption:
            KEYS['reminder_error'] = 'Lenght reminder text should be more 8 letter'
            return aiohttp_jinja2.render_template('index.html', request, context=KEYS)
        except ContentSpaceExeption:
            KEYS['reminder_error'] = 'You remonder have more space and less letter, correct pls'
            return aiohttp_jinja2.render_template('index.html', request, context=KEYS)
        except TimePassedExeption:
            KEYS['reminder_error'] = 'you set time is passed, correct date and time pls'
            return aiohttp_jinja2.render_template('index.html', request, context=KEYS)
        except EmptyDataExeption:
            KEYS['reminder_error'] = 'pls set date and time values'
            return aiohttp_jinja2.render_template('index.html', request, context=KEYS)

        # write in DB
        reminder = Reminder(content=content, departure_date=datetime_departure, user_id=int(user_id))
        async with await db.session() as session:
            try:
                session.add(reminder)
                await session.commit()
                log.critical(f'CREATE REMINDER IN DB WITH CONTENT {content}')
            except:
                log.critical('DB ERROR, REMINDER NOT COMMIT')
                await session.rollback()
        
        return web.HTTPFound(location='/')