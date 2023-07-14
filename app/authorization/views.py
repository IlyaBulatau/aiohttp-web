from aiohttp_security import remember
from aiohttp import web
import aiohttp_jinja2

from database.models import User
from sqlalchemy import select

@aiohttp_jinja2.template('login.html')
async def login(request: web.Request):
    method = request.method.upper()
    db = request.app['db']

    if method == 'GET':
        return {'title': 'login', 'header': 'Login Page'}
    
    elif method == 'POST':
        form_data = await request.post()
        email = form_data.get('email')

        async with await db.session() as session:
            query = select(User).filter(User.email == email)
            search = await session.execute(query)
            user = search.scalars().first()

        if user:
            print(user.email)
            await remember(request, web.HTTPFound('/'), str(user.id))
            return web.HTTPFound(location='/')
        else:
            print('user not found')
            return web.HTTPFound(location='/login')

async def signup(request):
    ...

async def logout(request):
    ...