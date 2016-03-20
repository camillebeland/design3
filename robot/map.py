import numpy as np


def cos(angle):
    return np.cos(angle/180 * np.pi)


def sin(angle):
    return np.sin(angle/180 * np.pi)


def rotation_matrix(theta):
    return np.array([[cos(theta), -1*sin(theta)], [sin(theta), cos(theta)]])


def rotate_vector(theta, vector):
    return np.dot(rotation_matrix(theta), vector)


class Map:
    def __init__(self, width, height):
        self._width = width
        self._height = height
        self._robot_position = np.array([width / 2, height / 2])
        self._robot_angle = 0;

    def set_robot_position(self, x, y):
        self._robot_position = np.array([x, y])

    def set_robot_angle(self, angle):
        self._robot_angle = angle

    def get_robot_position(self):
        return self._robot_position.tolist()

    def get_robot_angle(self):
        return self._robot_angle

    def get_robot_angle(self):
        return self._robot_angle

    def get_recharge_station_position(self):
        #TODO
        return (730,500)

    def get_treasure_closest_to(self, position):
        #TODO
        pass

    def find_island_with_clue(self, clue):
        #TODO
        pass

    def move_robot(self, delta_x, delta_y):
        delta = rotate_vector(- self._robot_angle, np.array([delta_x, delta_y]))
        self.set_robot_position(self._robot_position[0] + delta[0], self._robot_position[1] + delta[1])

    def rotate_robot(self, angle):
        self._robot_angle += angle
        self._robot_angle = self._robot_angle % 360

    def __is_inside_boundaries(self,x, y):
        return x > 0 and x < self._width and y > 0 and y < self._height

    def relative_position(self, position):
        return rotate_vector(self._robot_angle, np.array(position) - np.array(self._robot_position))
