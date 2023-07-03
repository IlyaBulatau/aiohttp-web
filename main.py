import argparse
import aioreloader
from aiohttp.web import Application, run_app
import aiohttp_jinja2
import jinja2
from app import setup_routes
from config.config import load_config


def setup_templates(application: Application):
    """
    Задает путь к папке с html шаблонами
    """
    aiohttp_jinja2.setup(application, loader=jinja2.FileSystemLoader(searchpath='templates'))



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
    

def setup_app(aplication: Application):
    """
    Настраивает приложения
    """
    setup_routes(aplication)
    setup_templates(aplication)
    setup_config(app, args.config)

app = Application()
args = parser_args()


if __name__ == "__main__":
    setup_app(app)
    run_app(app, host=args.host, port=args.port)
