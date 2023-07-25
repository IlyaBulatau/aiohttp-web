from celery import Celery
from celery.result import AsyncResult

from aiohttp import web


class CeleryServer:

    def __init__(self, app: web.Application):
        self.__app = app
        self.__rabbit = f'amqp://{self.__app["config"]["rabbit_user"]}:{self.__app["config"]["rabbit_password"]}@{self.__app["config"]["rabbit_host"]}//'
        self.__backend = 'rpc://'
        self.__server = Celery('mailings', broker=self.__rabbit, backend=self.__backend)

    @property
    def server(self):
        return self.__server

