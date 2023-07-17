from aiohttp_security import remember, forget
from aiohttp import web
import aiohttp_jinja2

from database.models import User
from sqlalchemy import select
from utils.validaters import auth_verification
from utils.log import log

from argon2 import PasswordHasher

@aiohttp_jinja2.template('login.html')
async def login(request: web.Request):
    method = request.method.upper()
    db = request.app['db']

    if method == 'GET':
        return {'title': 'Login', 'header': 'Login Page'}
    
    elif method == 'POST':
        form_data = await request.post()
        email = form_data.get('email')
        password = form_data.get('password')

        # if data empty
        if email == '' or password == '':
            log.warning('Empty Data')
            return web.HTTPFound('/login')
        
        #get user by email
        async with await db.session() as session:
            query = select(User).filter(User.email == email)
            search = await session.execute(query)
            user = search.scalars().first()

        # if user search
        if user:
            ph = PasswordHasher() # password hash object
            try:
                if ph.verify(user.password, password):
                    log.warning(f'Login {user.email}')
                    await remember(request, web.HTTPFound('/'), str(user.id))
                    return web.HTTPFound(location='/')
            except:
                log.warning('Incorrect password')
                return web.HTTPFound('/login')
            
        # if user not found
        else:
            log.warning('user not found')
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
        password = form_data.get('password')

        # validating data
        if username == '' or email == '' or password == '':
            log.warning('Not valid data')
            return web.HTTPFound('/signup')

        # seacrh user with this is email
        async with await db.session() as session:
            query = select(User).filter(User.email == email)

            search = await session.execute(query)
            user = search.scalars().first()
        
        # if has user
        if user:
            log.warning('This is email is exist')
            return web.HTTPFound('/signup')
                
        async with await db.session() as session:
            user = User(username=username, email=email, password=password)
            try:
                session.add(user)
                await session.commit()
            except:
                await session.rollback()
                log.critical('DB ERROR USER NOT COMMIT')

        return web.HTTPFound('/login')

@auth_verification
async def logout(request):
    await forget(request, web.HTTPFound('/'))
    return web.HTTPFound('/login')