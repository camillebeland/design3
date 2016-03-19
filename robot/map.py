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

    def move_robot(self, delta_x, delta_y):
        raise NotImplementedError

    def rotate_robot(self, angle):
        self._robot_angle += angle
        self._robot_angle = self._robot_angle % 360

    def __is_inside_boundaries(self,x, y):
        return x > 0 and x < self._width and y > 0 and y < self._height

    def relative_position(self, position):
        raise NotImplementedError