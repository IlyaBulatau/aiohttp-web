from aiohttp.web import HTTPException, middleware
from aiohttp import web
import aiohttp_jinja2

@middleware
async def error_middleware(request: web.Request, handler):
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

        elif status_code == 501:
            message = 'Sorry, we trash, pls try to comeback later'
        return aiohttp_jinja2.render_template('error.html', request, context={'status':status_code, 'message': message})    


