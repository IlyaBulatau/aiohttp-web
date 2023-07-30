import argparse
from aiohttp.web import Application, run_app
import aiohttp_jinja2
import jinja2
import aioredis
import aiohttp_session as AS
from aiohttp_session.redis_storage import RedisStorage

from database.connect import Database
from app import setup_routes, setup_seciruty, error_middleware
from config.config import load_config
from utils.log import log
from utils.validaters import add_keys_for_request_middleware


def setup_templates(application: Application):
    """
    Задает путь к папке с html шаблонами
    """
    aiohttp_jinja2.setup(application, loader=jinja2.FileSystemLoader(searchpath='templates'))
    application['static_root_url'] = '/static'


def parser_args():
    """
    Задает аргументы для запуска скрпта
    """
    parser = argparse.ArgumentParser()
    parser.add_argument('--host', help='Host arg')
    parser.add_argument('--port', help='Port arg')
    parser.add_argument('--config', type=argparse.FileType(), help='read config file')

    return parser.parse_args()

def setup_config(application: Application, config: dict):
    """
    Добавляет словарь конфигураций к приложению
    """
    application['config'] = load_config(config)
    
def setup_storage(application):
    AS.setup(application, RedisStorage(application['cache']))

def setup_app(application: Application):
    """
    Настраивает приложения
    """
    setup_routes(application)
    setup_templates(application)
    setup_config(app, args.config)
    app['cache'] = aioredis.from_url(f'redis://{app["config"]["redis_host"]}', encoding='utf-8', decode_responses=True)
    app['db'] = Database(app)
    setup_storage(application)
    setup_seciruty(application)    

    
app = Application(middlewares=[add_keys_for_request_middleware, error_middleware])
args = parser_args()

if __name__ == "__main__":
    setup_app(app)
    log.warning('RUN SERVER')
    run_app(app)
    log.warning('STOP SERVER')
    

 # TODO - настроить сессии что бы могли ондновременно существовать несколько юзеров
