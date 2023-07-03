from app.reminder import views
from aiohttp import web


def setup_routes(application: web.Application):
    application.router.add_get('/', views.index)