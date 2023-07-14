import aiohttp_jinja2
from aiohttp import web
from database.models import Reminder

from datetime import datetime


@aiohttp_jinja2.template('index.html')
async def index(request: web.Request):
    method = request.method.upper()
    db = request.app['db']

    if method == 'GET':
        return {'text': 'Main Page', 'title': 'Reminder'}

    elif method == 'POST':
        responce = await request.text()
        content = responce.split('=')[1].replace('+', ' ')
        reminder = Reminder(content=content, create_time=datetime.now(), user_id=1)
        async with await db.session() as session:
            session.add(reminder)
            await session.commit()
        
        return web.HTTPFound(location='/')