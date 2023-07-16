from aiohttp.web import HTTPFound, Request
from aiohttp_security import is_anonymous
import functools

def auth_verification(func):
    """
    For check auth user
    if user not auth - redirect /login page

    Used for routers
    """
    @functools.wraps(func)
    async def wrapper(*args, **kwargs):
        request: Request = args[0]
        anonymous = await is_anonymous(request)

        if anonymous:
            print('User not authorizade')
            return HTTPFound('/login')
        
        return await func(*args, **kwargs)
    
    return wrapper