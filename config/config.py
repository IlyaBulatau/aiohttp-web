from pathlib import Path
import yaml

def load_config(config_file=None):
    """
    Загружает из yaml файла конфиги в словарь
    """
    if not config_file:
        config_file =  Path(__file__).parent / 'config.yaml'   
    with open(config_file, 'r') as f:
        config = yaml.safe_load(f)


    return config
