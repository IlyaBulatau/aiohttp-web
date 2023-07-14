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
        return {'title': 'Login', 'header': 'Login Page'}
    
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

@aiohttp_jinja2.template('signup.html')
async def signup(request: web.Request):
    method = request.method.upper()
    db = request.app['db']

    if method == 'GET':
        return {'title': 'SignUp', 'header': 'SignUp Page'}

    elif method == 'POST':
        form_data = await request.post()
        username = form_data.get('username')
        email = form_data.get('email')
        
        # validating data
        if username == '' or email == '':
            print('Not valid data')
            return web.HTTPFound('/signup')

        # seacrh user with this is email
        async with await db.session() as session:
            query = select(User).filter(User.email == email)

            search = await session.execute(query)
            user = search.scalars().first()
        
        # if has user
        if user:
            print('This is email is exist')
            return web.HTTPFound('/signup')
        
        async with await db.session() as session:
            user = User(username=username, email=email)
            session.add(user)
            await session.commit()
        return web.HTTPFound('/login')

async def logout(request):
    ...