from celery import Celery

from aiohttp import web


class CeleryServer:

    def __init__(self, app: web.Application):
        self.__app = app
        self.__rabbit = 'pyamqp://guest@localhost//'
        self.__server = Celery('mailings', broker=self.__rabbit)

    @property
    def server(self):
        return self.__server

celery = CeleryServer('s').server