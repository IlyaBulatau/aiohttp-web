from app.reminder import views
from aiohttp import web
from app.authorization import views as views_auth


def setup_routes(application: web.Application):
    application.router.add_get('/', views.index, name='index')
    application.router.add_post('/', views.index)
    application.router.add_get('/login', views_auth.login, name='login')
    application.router.add_post('/login', views_auth.login)
    application.router.add_get('/signup', views_auth.signup, name='signup')
    application.router.add_post('/signup', views_auth.signup)
    application.router.add_get('/logout', views_auth.logout, name='logout')

    application.router.add_static(prefix='/static', path='static/css', name='static')
