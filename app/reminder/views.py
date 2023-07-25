import aiohttp_jinja2
from aiohttp import web
from aiohttp_security import authorized_userid
from sqlalchemy import select

from utils.log import log
from utils.schemes import ReminderSaveForm
from utils.validaters import auth_verification
from utils.smtp_process.smtp_service import mailing

from database.models import Reminder, User
from datetime import datetime
from database.connect import Database
from app.exeption.processing import error_controller


@aiohttp_jinja2.template('index.html')
@error_controller(template_name='index.html', title='Reminder', header='Main Page')
@auth_verification
async def index(request: web.Request):

    user_id: int = await authorized_userid(request)
    log.warning(f'User activate login in ID: {user_id}')
    
    method: str = request.method.upper()
    db: Database = request.app['db']

    if method == 'GET':
        return request['KEYS']

    elif method == 'POST':
        responce: dict = await request.post()

        # get data
        content: str = responce.get('reminder')
        date_departure: str = responce.get('calendar')
        time_departure: str = responce.get('time')
        
        # validate dataset
        ReminderSaveForm(content=content, date_departure=date_departure, time_departure=time_departure)
        datetime_departure = datetime.strptime(date_departure+'/'+time_departure, '%Y-%m-%d/%H:%M')
        
        # write in DB
        reminder = Reminder(content=content, departure_date=datetime_departure, user_id=int(user_id))
        async with await db.session() as session:
            try:
                session.add(reminder)
                await session.commit()
                log.critical(f'CREATE REMINDER IN DB WITH CONTENT {content}')
            except Exception as e:
                log.critical(f'DB ERROR, REMINDER NOT COMMIT\n{e}')
                await session.rollback()
                return aiohttp_jinja2.render_template('error.html', request, context={'status': 500, 'message': 'Sorry our server is down, please try again later'})
        
        #get user email
        async with await db.session() as session:
            query = select(User).filter(User.id == int(user_id))
            try:
                search = await session.execute(query)
                user: User = search.scalars().first()
            except Exception as e:
                log.critical(f'DOWN DB {e}')
                await session.rollback()

        # create shedule task to mailing user reminder
        mailing.delay(request.app['config']['app_mail'],
                      request.app['config']['app_mail_password'],
                      user.email,
                      reminder.content)

        log.warning(f'User by ID {user_id} create task')
        
        return web.HTTPFound(location='/reminders')
    
@aiohttp_jinja2.template('reminders.html')
@error_controller(template_name='reminders.html', title='Reminders List', header='You Reminders')
@auth_verification
async def reminders(request: web.Request):

    user_id = int(await authorized_userid(request))
    db: Database = request.app['db']

    async with await db.session() as session:
        query = select(Reminder).filter(Reminder.user_id == user_id)

        search = await session.execute(query)
        reminders = search.scalars().all()
        
    request['KEYS']['reminders_active'] = [r for r in reminders if r.departure_date > datetime.now()]
    request['KEYS']['reminders_later'] = [r for r in reminders if r.departure_date <= datetime.now()]
    return request['KEYS']

