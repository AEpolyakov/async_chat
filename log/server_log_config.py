import logging
from logging.handlers import RotatingFileHandler
import os


handler = RotatingFileHandler(filename=os.path.join('.', 'log', 'server.log'), maxBytes=2000, backupCount=10)
formater = logging.Formatter("%(asctime)s %(levelname)s %(pathname)s %(message)s")
handler.setFormatter(formater)

server_logger = logging.getLogger('server_log')
server_logger.addHandler(handler)
server_logger.setLevel(logging.INFO)
