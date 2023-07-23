from aiohttp.web import HTTPFound, Request, middleware
from aiohttp_security import is_anonymous
import functools
from typing import Callable

KEYS = {'title': None, 
        'header': None, 
        'username_error': None, 
        'password_error': None, 
        'email_error': None, 
        'reminder_error': None,
        }

def auth_verification(func: Callable):
    """
    For check auth user
    if user not auth - redirect /login page

    Used for routers
    """
    @functools.wraps(func)
    async def wrapper(*args, **kwargs):
        request: Request = args[0]
        anonymous: int = await is_anonymous(request)

        if anonymous:
            print('User not authorizade')
            return HTTPFound('/login')
        
        return await func(*args, **kwargs)
    
    return wrapper


@middleware
async def add_keys_for_request_middleware(request: Request, handler: Callable):
    """
    Adds all requests to KEYS, needed to transfer keys and values to html templates
    """
    request['KEYS'] = KEYS
    return await handler(request)