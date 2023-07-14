import argparse
from aiohttp.web import Application, run_app
import aiohttp_jinja2
import jinja2

from database.connect import Database
from app import setup_routes, setup_seciruty
from config.config import load_config

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
    

def setup_app(application: Application):
    """
    Настраивает приложения
    """
    setup_routes(application)
    setup_templates(application)
    setup_config(app, args.config)
    app['db'] = Database(app)
    setup_seciruty(application)

app = Application()
args = parser_args()

if __name__ == "__main__":
    setup_app(app)
    run_app(app, host=args.host, port=args.port)

 # TODO - сейчас данные авторизации хранятся как ключ приложения и при перезапуске не сохраняются, нужно перенести их в редис (aioredis)
 # TODO - сделать возможность выхода из профиля
 # TODO - привести в порядок маршрутизацию, сделать правильные редиректы
 # (условно после создания напоминания юзер должен перенапрявлятся на страницу с эти напоминанием)
 # TODO - отрефакторить шалоны, сделать 1 базовый, переписать ссылку на абстрактные, а не прямые
 # TODO - добавить pydantic для валидации данных плученных с html формы 
 # TODO - обрабатывать исключения и не валидные данные введенные в форме либо в строке поиска