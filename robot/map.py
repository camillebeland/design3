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
        self._robotPosition = np.array([width / 2, height / 2])
        self._robotAngle = 0;

    def set_robot_position(self, x, y):
        if not self.__is_inside_boundaries(x,y):
            raise Exception("Robot out of map boundaries : {0} , {1}".format(x,y))
        else:
            self._robotPosition = np.array([x, y])

    def set_robot_angle(self, angle):
        self._robotAngle = angle

    def get_robot_position(self):
        return self._robotPosition.tolist()

    def get_robot_angle(self):
        return self._robotAngle

    def get_robot_angle(self):
        return self._robotAngle

    def move_robot(self, delta_x, delta_y):
        delta = rotate_vector(- self._robotAngle, np.array([delta_x, delta_y]))
        self.set_robot_position(self._robotPosition[0] + delta[0], self._robotPosition[1] + delta[1])

    def rotate_robot(self, angle):
        self._robotAngle += angle
        self._robotAngle = self._robotAngle % 360

    def __is_inside_boundaries(self,x, y):
        return x > 0 and x < self._width and y > 0 and y < self._height

    def relative_position(self, position):
        return rotate_vector(self._robotAngle, np.array(position) - np.array(self._robotPosition))
