import logging

logging.basicConfig(filename='system.log',level=logging.DEBUG)


def warning(message):
    logging.warning(message)


def info(message):
    logging.info(message)