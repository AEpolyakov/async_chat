import logging
from logging.handlers import RotatingFileHandler

# handler = logging.FileHandler('client.log')
handler = RotatingFileHandler(filename='client.log', maxBytes=2000, backupCount=10)
formater = logging.Formatter("%(asctime)s %(levelname)s %(pathname)s %(message)s")
handler.setFormatter(formater)

client_logger = logging.getLogger('client_log')
client_logger.addHandler(handler)
client_logger.setLevel(logging.INFO)
