import aiohttp_jinja2
from aiohttp import web
from aiohttp_security import authorized_userid

from utils.log import log
from utils.validaters import auth_verification
from database.models import Reminder
from datetime import datetime


@aiohttp_jinja2.template('index.html')
@auth_verification
async def index(request: web.Request):

    user_id = await authorized_userid(request)
    log.warning(f'User activate login in ID: {user_id}')

    method = request.method.upper()
    db = request.app['db']

    if method == 'GET':
        return {'text': 'Main Page', 'title': 'Reminder'}

    elif method == 'POST':
        responce = await request.post()

        # get data
        content = responce.get('reminder')
        date_departure = responce.get('calendar')
        time_departure = responce.get('time')

        # validate dataset
        if content == ''\
        or date_departure == ''\
        or time_departure == '':
            log.warning('Empty Data')
            return web.HTTPFound(location='/')
        
        # time passed
        datetime_departure = datetime.strptime(date_departure+'/'+time_departure, '%Y-%m-%d/%H:%M')

        # validate time passed
        if datetime_departure < datetime.now():
            log.warning('Time has passed')
            return web.HTTPFound(location='/')

        # write in DB
        reminder = Reminder(content=content, departure_date=datetime_departure, user_id=int(user_id))
        async with await db.session() as session:
            try:
                session.add(reminder)
                await session.commit()
            except:
                log.critical('DB ERROR, REMINDER NOT COMMIT')
                await session.rollback()
        log.warning(content)        
        return web.HTTPFound(location='/')