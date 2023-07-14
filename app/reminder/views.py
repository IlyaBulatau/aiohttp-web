import aiohttp_jinja2
from aiohttp import web
from aiohttp_security import is_anonymous, authorized_userid

from sqlalchemy import select
from database.models import Reminder
from datetime import datetime


@aiohttp_jinja2.template('index.html')
async def index(request: web.Request):

    # auth verification
    user_is_anonymous= await is_anonymous(request) 
    # if user is anonymous - not auth
    if user_is_anonymous:
        print('User not authorizade')
        return web.HTTPFound('/login')
    else:
        user_id = await authorized_userid(request)
        print(f'User activate login in ID: {user_id}')
        

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
            print('Empty Data')
            return web.HTTPFound(location='/')
        
        # time passed
        datetime_departure = datetime.strptime(date_departure+'/'+time_departure, '%Y-%m-%d/%H:%M')

        # validate time passed
        if datetime_departure < datetime.now():
            print('Time has passed')
            return web.HTTPFound(location='/')

        # write in DB
        reminder = Reminder(content=content, departure_date=datetime_departure, user_id=int(user_id))
        async with await db.session() as session:
            session.add(reminder)
            await session.commit()
            
        print(content)        
        return web.HTTPFound(location='/')