import argparse
from aiohttp.web import Application, run_app
import aiohttp_jinja2
import jinja2
import aioredis
import aiohttp_session as AS
from aiohttp_session.redis_storage import RedisStorage

from database.connect import Database
from app import setup_routes, setup_seciruty
from config.config import load_config
from utils import log

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
    parser.add_argument('--host', help='Host arg', default='0.0.0.0')
    parser.add_argument('--port', help='Port arg', default=8080)
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
    
app = Application()
args = parser_args()

if __name__ == "__main__":
    setup_app(app)
    log.warning('RUN SERVER')
    run_app(app, host=args.host, port=args.port)
    log.warning('STOP SERVER')
    

 # TODO - настроить сессии что бы могли ондновременно существовать несколько юзеров
 # TODO - привести в порядок маршрутизацию, сделать правильные редиректы
 # (условно после создания напоминания юзер должен перенапрявлятся на страницу с эти напоминанием)

 # TODO - отрефакторить шалоны, сделать 1 базовый, переписать ссылку на абстрактные, а не прямые
 # TODO - добавить селери для отправки напоминаний на почту
 # TODO - доделать ошибки обрабатывающие не валидные данные с форм и сделать обработку http ошибок
 