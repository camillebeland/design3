import logging


class Logger:
    def __init__(self):
        self.logging = logging
        self.logging.basicConfig(filename='system.log', filemode='w', level=logging.DEBUG, format='%(asctime)s %(message)s')

    def warning(self, message):
        self.logging.warning(message)

    def info(self, message):
        self.logging.info(message)

    def inject_mock_logging(self, mock_logging):
        self.logging = mock_logging
