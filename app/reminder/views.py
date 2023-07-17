import aiohttp_jinja2
from aiohttp import web
from aiohttp_security import authorized_userid

from utils import auth_verification, log, ReminderSaveForm
from database.models import Reminder
from datetime import datetime
from database.connect import Database


@aiohttp_jinja2.template('index.html')
@auth_verification
async def index(request: web.Request):

    user_id: int = await authorized_userid(request)
    log.warning(f'User activate login in ID: {user_id}')
    
    method: str = request.method.upper()
    db: Database = request.app['db']

    if method == 'GET':
        return {'text': 'Main Page', 'title': 'Reminder'}

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
        except:
            return web.HTTPFound('/')
        
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