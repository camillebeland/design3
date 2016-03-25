from threading import Thread

import requests


class VisionDaemon:
    def __init__(self, base_station_address, assembler):
        self.base_station_address = base_station_address
        self.last_robot_info_from_vision = dict()
        self.robot_info_assembler = assembler
        self.start_fetching_robot_position_from_vision()

    def get_robot_position_from_vision(self):
            return self.last_robot_info_from_vision

    def get_robot_angle_from_vision(self):
        return self.last_robot_position_from_vision['angle']

    def __fetch_robot_position_from_vision__(self):
        while self.running:
            try:
                response = requests.get(str(self.base_station_address) + '/vision/robot')
                response.raise_for_status()
                if not response.json():
                    print("Robot position is not found, base station returned nothing")
                else:
                    robot_info_json = response.json()
                    robot_info = self.robot_info_assembler.json_to_robot_info(robot_info_json)
                    self.last_robot_info_from_vision = robot_info
            except requests.exceptions.RequestException:
                print('can\'t fetch robot position from vision ' + str(self.base_station_address) + ' is not available')

    def start_fetching_robot_position_from_vision(self):
        self.thread = Thread(target=self.__fetch_robot_position_from_vision__)
        self.running = True
        self.thread.start()

    def stop_fetching_robot_position_from_vision(self):
        self.running = False
