from app.reminder import views
from aiohttp import web
from app.authorization import views as views_auth


def setup_routes(application: web.Application):
    application.router.add_get('/', views.index)
    application.router.add_post('/', views.index)
    application.router.add_get('/login', views_auth.login)
    application.router.add_post('/login', views_auth.login)

    application.router.add_static(prefix='/static', path='static/css', name='static')
