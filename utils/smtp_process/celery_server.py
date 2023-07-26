from celery import Celery

from aiohttp import web
from config.config import load_config


def make_celery():
    """
    Create Celery instance
    """
    data: dict = load_config()
    user = data.get('rabbit_user')
    password = data.get('rabbit_password')
    host = data.get('rabbit_host')
    celery = Celery(__name__, broker=f'amqp://{user}:{password}@{host}//', backend='rpc://')
    celery.conf.timezone = 'Europe/Minsk' 


    return celery
