import logging

log = logging.getLogger(__name__)
log.setLevel('DEBUG')

formatter = logging.Formatter(fmt='{asctime} | {levelname} | {message}', style='{')

file_handler = logging.FileHandler(filename='log.log', mode='a', encoding='utf-8')
file_handler.setLevel('DEBUG')
file_handler.setFormatter(formatter)

console_handler = logging.StreamHandler()
console_handler.setLevel('DEBUG')
console_handler.setFormatter(formatter)

log.addHandler(file_handler)
log.addHandler(console_handler)