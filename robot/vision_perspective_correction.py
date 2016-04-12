
class VisionPerspectiveCorrection:
    def __init__(self, actual_vision, camera_position, camera_height, robot_height):
        self.__actual_vision = actual_vision
        self.__correction_factor = 1.0 - (robot_height / camera_height)
        self.__camera_position = camera_position

    def get_robot_position_from_vision(self):
        perspective_position = self.__actual_vision.get_robot_position_from_vision()
        corrected_position = ((perspective_position - self.__camera_position) * self.__correction_factor) + self.__camera_position
        return corrected_position

    def get_robot_angle_from_vision(self):
        return self.__actual_vision.get_robot_angle_from_vision()
