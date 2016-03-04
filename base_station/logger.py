import logging


class Logger:
    def __init__(self):
        logging.basicConfig(filename='system.log',level=logging.DEBUG)

    def warning(self, message):
        logging.warning(message)

    def info(self, message):
        logging.info(message)