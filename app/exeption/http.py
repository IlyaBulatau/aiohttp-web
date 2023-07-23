from aiohttp import web
import aiohttp_jinja2
from typing import Callable

@web.middleware
async def error_middleware(request: web.Request, handler: Callable):
    """
    This is middleware check and processing http errors
    """
    message = None

    try:
        responce: web.Response = await handler(request)
        return responce
    except web.HTTPException as e:
        status_code = int(e.status)

        if status_code == 404:
            message = 'The URL not found' 
            
        elif status_code == 408:
            message = 'Timeout Request, check you connect with Internet'

        elif int(str(status_code)[0]) == 5:
            message = 'Sorry, we trash, pls try to comeback later'
        return aiohttp_jinja2.render_template('error.html', request, context={'status':status_code, 'message': message})    


