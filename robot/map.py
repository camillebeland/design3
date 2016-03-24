import numpy as np


class Map:
    def __init__(self, width, height, vision_daemon):
        self._width = width
        self._height = height
        self._robot_angle = 0
        self.vision_daemon = vision_daemon

    def set_robot_angle(self, angle):
        self._robot_angle = angle

    def get_robot_position(self):
        return self.vision_daemon.get_robot_position_from_vision()

    def get_robot_angle(self):
        return self._robot_angle

    def relative_position(self, position):
        return rotate_vector(self._robot_angle, np.array(position) - np.array(self._robot_position))

    def get_recharge_station_position(self):
        #TODO
        return (1500,1000)

    def get_treasure_closest_to(self, position):
        #TODO
        pass

    def find_island_with_clue(self, clue):
        #TODO
        pass


def rotate_vector(theta, vector):
    return np.dot(rotation_matrix(theta), vector)


def cos(angle):
    return np.cos(angle/180 * np.pi)


def sin(angle):
    return np.sin(angle/180 * np.pi)


def rotation_matrix(theta):
    return np.array([[cos(theta), -1*sin(theta)], [sin(theta), cos(theta)]])
