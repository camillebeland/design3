import numpy as np
from utils.position import Position


def cos(angle):
    return np.cos(angle/180 * np.pi)


def sin(angle):
    return np.sin(angle/180 * np.pi)


def rotation_matrix(theta):
    return np.array([[cos(theta), -1*sin(theta)], [sin(theta), cos(theta)]])


def rotate_vector(theta, vector):
    return np.dot(rotation_matrix(theta), vector)


class SimulationMap:
    def __init__(self, width, height):
        self._width = width
        self._height = height
        self._robot_position = Position(width / 2, height / 2)
        self._robot_angle = 0

    def set_robot_position(self, x, y):
        self._robot_position = Position(x, y)

    def set_robot_angle(self, angle):
        self._robot_angle = angle

    def get_robot_position(self):
        return self._robot_position

    def get_robot_angle(self):
        return self._robot_angle

    def get_recharge_station_position(self):
        #TODO
        return (1500,1000)

    def get_treasure_closest_to(self, position):
        #TODO
        pass

    def find_island_with_clue(self, clue):
        #TODO
        pass

    def move_robot(self, delta_x, delta_y):
        delta = rotate_vector(- self._robot_angle, np.array([delta_x, delta_y]))
        self.set_robot_position(self._robot_position.x + delta[0], self._robot_position.y + delta[1])

    def rotate_robot(self, angle):
        self._robot_angle += angle
        self._robot_angle = self._robot_angle % 360

    def __is_inside_boundaries(self,x, y):
        return x > 0 and x < self._width and y > 0 and y < self._height

    def relative_position(self, position):
        return rotate_vector(self._robot_angle, np.array(position.x, position.y) - np.array(self._robot_position.x, self._robot_position.y))
