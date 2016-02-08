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
        self._robotposition = np.array([width/2, height/2])
        self._robotangle = 0;

    def get_robot_position(self):
        return self._robotposition.tolist()

    def get_robot_angle(self):
        return self._robotangle

    def move_robot(self, delta_x, delta_y):
        delta = rotate_vector(- self._robotangle, np.array([delta_x, delta_y]))
        self._robotposition += delta

    def rotate_robot(self, angle):
        self._robotangle += angle
