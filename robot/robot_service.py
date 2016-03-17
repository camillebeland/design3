import requests


class RobotService:
    def __init__(self, base_station_address):
        self.base_station_address = base_station_address

    def log_info(self, message_to_log):
        requests.post(str(self.base_station_address)+"/logger/info", json={'message': message_to_log})

    def fetch_robot_position_from_vision(self):
        try:
            self.robot_position_from_vision = requests.get(str(self.base_station_address)+ '/robot_position')
        except requests.exceptions.RequestException:
            print('can\'t fetch robot position from vision' + str(self.base_station_address) + ' is not available')
        if not self.robot_position_from_vision.json():
            self.log_info("Robot position is not found")
        else:
            return self.robot_position_from_vision.json()
