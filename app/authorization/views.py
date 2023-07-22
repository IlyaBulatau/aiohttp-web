from aiohttp_security import remember, forget, is_anonymous
from aiohttp import web
import aiohttp_jinja2

from database.models import User
from database.connect import Database
from sqlalchemy import select
from utils import auth_verification, log, UserSignUpForm, UserLoginForm
from app.exeption.values_exeption import (PasswordLenghtExeption,
                PasswordLetterExeption,
                PasswordNotHaveDigit,
                PasswordSpaceExeption,
                PasswordStrExeption,
                UsernameHavePunctuationsExeption,
                UsernameLenghtExeption,
                UsernameSpaceExeption,
                UsernameStrExeption)

from email_validator.exceptions_types import EmailNotValidError

from argon2 import PasswordHasher

@aiohttp_jinja2.template('login.html')
async def login(request: web.Request):
    KEYS = {'title': 'Login', 'header': 'Login Page', 'password_error': None, 'email_error': None}

    # user auth redirect "/" page 
    if not await is_anonymous(request):
        return web.HTTPFound('/')
    
    method: str = request.method.upper()
    db: Database = request.app['db']
    
    if method == 'GET':
        return KEYS
    
    elif method == 'POST':
        form_data: dict = await request.post()
        email = form_data.get('email')
        password = form_data.get('password')

        # validate data
        try:
            UserLoginForm(email=email, password=password)
        except PasswordLenghtExeption:
            KEYS['password_error'] = 'passport lenght need be more 8 symbols'
            return aiohttp_jinja2.render_template('login.html', request, context=KEYS)
        except PasswordLetterExeption:
            KEYS['password_error'] = 'password must contain at least 4 different English letters'
            return aiohttp_jinja2.render_template('login.html', request, context=KEYS)
        except PasswordNotHaveDigit:
            KEYS['password_error'] = 'password most be contain digit'
            return aiohttp_jinja2.render_template('login.html', request, context=KEYS)
        except PasswordSpaceExeption:
            KEYS['password_error'] = 'password most be not have space'
            return aiohttp_jinja2.render_template('login.html', request, context=KEYS)
        except PasswordStrExeption:
            KEYS['password_error'] = 'you password empty or dont have letter'
            return aiohttp_jinja2.render_template('login.html', request, context=KEYS)
        except Exception:
            KEYS['email_error'] = 'email invalid'
            return aiohttp_jinja2.render_template('login.html', request, context=KEYS)
            
        
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
                KEYS['password_error'] = 'Incorrect password'
                return aiohttp_jinja2.render_template('index.html', request, context=KEYS)
            
        # if user not found
        else:
            log.warning('user not found')
            KEYS['email_error'] = 'user not found'
            return aiohttp_jinja2.render_template('index.html', request, context=KEYS)



@aiohttp_jinja2.template('signup.html')
async def signup(request: web.Request):
    KEYS = {'title': 'SingUp', 'header': 'SignUp Page', 'password_error': None, 'email_error': None, 'username_error': None}

    method: str = request.method.upper()
    db: Database = request.app['db']
    
    if method == 'GET':
        return {'title': 'SignUp', 'header': 'SignUp Page'}

    elif method == 'POST':
        form_data: dict = await request.post()
        username = form_data.get('username')
        email = form_data.get('email')
        password = form_data.get('password')

        # validating data
        try:
            UserSignUpForm(username=username, email=email, password=password)
        except UsernameStrExeption:
            KEYS['username_error'] = 'user name is empty or not have letter'
            return aiohttp_jinja2.render_template('signup.html', request, context=KEYS)
        except UsernameLenghtExeption:
            KEYS['username_error'] = 'username should be lenght more 1 letter'
            return aiohttp_jinja2.render_template('signup.html', request, context=KEYS)
        except UsernameSpaceExeption:
            KEYS['username_error'] = 'username sould be dont have spaces'
            return aiohttp_jinja2.render_template('login.html', request, context=KEYS)
        except PasswordLenghtExeption:
            KEYS['password_error'] = 'passport lenght need be more 8 symbols'
            return aiohttp_jinja2.render_template('signup.html', request, context=KEYS)
        except PasswordLetterExeption:
            KEYS['password_error'] = 'password must contain at least 4 different English letters'
            return aiohttp_jinja2.render_template('signup.html', request, context=KEYS)
        except PasswordNotHaveDigit:
            KEYS['password_error'] = 'password most be contain digit'
            return aiohttp_jinja2.render_template('signup.html', request, context=KEYS)
        except PasswordSpaceExeption:
            KEYS['password_error'] = 'password most be not have space'
            return aiohttp_jinja2.render_template('signup.html', request, context=KEYS)
        except PasswordStrExeption:
            KEYS['password_error'] = 'you password empty or dont have letter'
            return aiohttp_jinja2.render_template('signup.html', request, context=KEYS)
        except UsernameHavePunctuationsExeption:
            KEYS['username_error'] = 'error you user name have punctuation symbols'
            return aiohttp_jinja2.render_template('signup.html', request, context=KEYS)
        except Exception:
            KEYS['email_error'] = 'email invalid'
            return aiohttp_jinja2.render_template('login.html', request, context=KEYS)
        
        # seacrh user with this is email
        async with await db.session() as session:
            query = select(User).filter(User.email == email)

            search = await session.execute(query)
            user = search.scalars().first()
        
        # if has user
        if user:
            log.warning('This is email is exist')
            KEYS['email_error'] = 'this is email is exist'
            return aiohttp_jinja2.render_template('signup.html', request, context=KEYS)
                
        async with await db.session() as session:
            user = User(username=username, email=email, password=password)
            try:
                log.critical(f'ADD NEW USER WITH EMAIL {user.email}')
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