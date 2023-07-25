from aiohttp_security import remember, forget, is_anonymous
from aiohttp import web
import aiohttp_jinja2

from database.models import User
from database.connect import Database
from sqlalchemy import select

from utils.validaters import auth_verification
from utils.schemes import UserLoginForm, UserSignUpForm
from utils.log import log

from app.exeption.processing import error_controller
from argon2 import PasswordHasher

@aiohttp_jinja2.template('login.html')
@error_controller(template_name='login.html', title='Login', header='Login Page')
async def login(request: web.Request):

    # if user auth - redirect "/" page 
    if not await is_anonymous(request):
        return web.HTTPFound('/')
    
    method: str = request.method.upper()
    db: Database = request.app['db']
    
    if method == 'GET':
        return request['KEYS']
    
    elif method == 'POST':
        # get data from html form
        form_data: dict = await request.post()
        email: str = form_data.get('email')
        password: str = form_data.get('password')

        # validate data
        UserLoginForm(email=email, password=password)

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
                    # remember current user
                    await remember(request, web.HTTPFound('/'), str(user.id)) 
                    return web.HTTPFound(location='/')
            except:
                msg = 'Incorrect password'
                log.warning(msg)
                request['KEYS']['password_error'] = msg
                return aiohttp_jinja2.render_template('login.html', request, context=request['KEYS'])
            
        # if user not found
        else:
            msg = 'user not found'
            log.warning(msg)
            request['KEYS']['email_error'] = msg
            return aiohttp_jinja2.render_template('login.html', request, context=request['KEYS'])



@aiohttp_jinja2.template('signup.html')
@error_controller(template_name='signup.html', title='SignUp', header='SignUp Page')
async def signup(request: web.Request):

    method: str = request.method.upper()
    db: Database = request.app['db']
    
    if method == 'GET':
        return request['KEYS']

    elif method == 'POST':
        # get data from html form
        form_data: dict = await request.post()
        username: str = form_data.get('username')
        email: str = form_data.get('email')
        password: str = form_data.get('password')

        # validating data
        UserSignUpForm(username=username, email=email, password=password)
        
        # seacrh user with this is email
        async with await db.session() as session:
            query = select(User).filter(User.email == email)
            search = await session.execute(query)
            user = search.scalars().first()
        
        # if has user
        if user:
            msg = 'This is email is exist'
            log.warning(msg)
            request['KEYS']['email_error'] = msg
            return aiohttp_jinja2.render_template('signup.html', request, context=request['KEYS'])
                
        async with await db.session() as session:
            user = User(username=username, email=email, password=password)
            try:
                log.critical(f'ADD NEW USER WITH EMAIL {user.email}')
                session.add(user)
                await session.commit()
            except:
                await session.rollback()
                log.critical('DB ERROR USER NOT COMMIT')
                return aiohttp_jinja2.render_template('error.html', request, context={'status': 500, 'message': 'Sorry our server is down, please try again later'})

        return web.HTTPFound('/login')

@auth_verification
async def logout(request):
    # forget currecnt user
    await forget(request, web.HTTPFound('/'))
    return web.HTTPFound('/login')