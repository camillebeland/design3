import numpy as np
from utils.position import Position
from utils.math import cos, sin, rotate_vector

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
        return Position(1500,1000)

    def get_treasure_closest_to(self, position):
        #TODO
        pass

    def find_island_with_clue(self, clue):
        #TODO
        pass

    def move_robot(self, delta_x, delta_y):
        delta = rotate_vector(- self._robot_angle, Position(delta_x, delta_y))
        self.set_robot_position(self._robot_position.x + delta[0], self._robot_position.y + delta[1])

    def rotate_robot(self, angle):
        self._robot_angle += angle
        self._robot_angle = self._robot_angle % 360

