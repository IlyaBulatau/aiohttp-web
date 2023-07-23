from aiohttp.web import HTTPFound, Request, middleware
from aiohttp_security import is_anonymous
import functools
from typing import Callable


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


