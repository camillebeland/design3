import threading
import time
from utils.position import Position

import requests
from robot.no_connection_exception import NoConnectionException


class VisionDaemon:
    def __init__(self, base_station_address, assembler, is_mock=False):
        self.base_station_address = base_station_address
        self.last_robot_info_from_vision = dict()
        self.robot_info_assembler = assembler
        self.start_fetching_robot_position_from_vision()
        self.is_mock = is_mock
        self.__connected = False

    def get_robot_position_from_vision(self):
        if self.__connected:
            if self.last_robot_info_from_vision:
                return Position(self.last_robot_info_from_vision['x'], self.last_robot_info_from_vision['y'])
            else:
                return Position(0, 0)
        else:
            raise NoConnectionException('Cannot connect to base station')

    def get_robot_angle_from_vision(self):
        if self.last_robot_info_from_vision:
            return self.last_robot_info_from_vision['angle']
        else:
            return 41

    def __fetch_robot_position_from_vision__(self):
        while self.running:
            time.sleep(0.05)
            try:
                response = requests.get(str(self.base_station_address) + '/vision/robot', timeout=0.3)
                response.raise_for_status()
                if not response.json():
                    pass
                else:
                    robot_info_json = response.json()
                    robot_info = self.robot_info_assembler.json_to_robot_info(robot_info_json)
                    self.last_robot_info_from_vision = robot_info
                self.__connected = True
            except requests.exceptions.RequestException:
                self.__connected = False
            if self.is_mock:
                break


    def start_fetching_robot_position_from_vision(self):
        print("Starting vision daemon")
        self.thread = threading.Thread(target=self.__fetch_robot_position_from_vision__)
        self.running = True
        self.thread.start()

    def stop_fetching_robot_position_from_vision(self):
        self.running = False
