import requests
from threading import Thread


class RobotService:
    def __init__(self, base_station_address, island_server_address):
        self.base_station_address = base_station_address
        self.island_server_address = island_server_address
        self.robot_position = []

    def log_info(self, message_to_log):
        requests.post(str(self.base_station_address)+"/logger/info", json={'message': message_to_log})

    def get_robot_position(self):
        return self.robot_position

    def __fetch_robot_position_from_vision__(self):
        while self.running:
            try:
                self.robot_position_from_vision = requests.get(str(self.base_station_address)+ '/robot_position')
            except requests.exceptions.RequestException:
                print('can\'t fetch robot position from vision ' + str(self.base_station_address) + ' is not available')
            if not self.robot_position_from_vision.json():
                self.log_info("Robot position is not found")
            else:
                self.robot_position = self.robot_position_from_vision.json()

    def start_fetching_robot_position_from_vision(self):
        self.thread = Thread(target=self.__fetch_robot_position_from_vision__)
        self.running = True
        self.thread.start()

    def stop_fetching_robot_position_from_vision(self):
        self.running = False

    def ask_target_island(self, manchester_letter):
        payload = {'code': manchester_letter}
        care_about_ssl_certificate = False
        response = requests.get(str(self.island_server_address), params=payload, verify=care_about_ssl_certificate)
        return response.text
