import threading
import requests


class RobotVisionDaemon:
    def __init__(self, robot_address, vision_service, camera_position, camera_height, robot_height):
        self.robot_address = robot_address
        self.vision = vision_service
        self.__correction_factor = 1.0 - (robot_height / camera_height)
        self.__camera_position = camera_position
        self.start_thread()

    def __post_robot_info_from_vision_to_robot__(self):
        while self.running:
            robot_info_from_vision = self.vision.find_robot_position()
            robot_info_corrected = self.__adjust_for_perspective(robot_info_from_vision)
            try:
                response = requests.post(str(self.robot_address) + '/vision/robot', robot_info_corrected.to_dict())
                response.raise_for_status()
            except requests.exceptions.RequestException:
                print('can\'t post robot position from vision to robot' + str(self.robot_address) + ' is not available')

    def start_thread(self):
        print("Starting vision daemon")
        self.thread = threading.Thread(target=self.__post_robot_info_from_vision_to_robot__)
        self.running = True
        self.thread.start()

    def __adjust_for_perspective(self, robot_info):
        corrected_position = ((robot_info.position - self.__camera_position) * self.__correction_factor) + self.__camera_position
        robot_info.position = corrected_position
        return robot_info



