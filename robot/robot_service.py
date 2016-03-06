import urllib
import json
from urllib.error import HTTPError
import requests


class RobotService:

    def __init__(self, base_station_address):
        self.base_station_address = base_station_address

    def log_info(self, message_to_log):
        requests.post(str(self.base_station_address)+"/logger/info", json={'message': message_to_log})

