import numpy as np
from utils.position import Position
from utils.math import cos, sin, rotate_vector

class SimulationMap:
    def __init__(self, width, height, worldmap_service):
        self._width = width
        self._height = height
        self._robot_position = Position(width / 2, height / 2)
        self._robot_angle = 0
        self.worldmap_service = worldmap_service

    def set_robot_position(self, x, y):
        self._robot_position = Position(x, y)

    def set_robot_angle(self, angle):
        self._robot_angle = angle

    def get_robot_position(self):
        return self._robot_position

    def get_robot_angle(self):
        return self._robot_angle

    def get_recharge_station_position(self):
        position = self.worldmap_service.get_charging_station_position()
        charging_station_position = Position(position["x"], position["y"])
        return charging_station_position

    def get_treasure_closest_to(self, position):
        #TODO
        return Position(500,600)

    def find_island_with_clue(self, clue):
        #TODO
        return Position(500,500)

    def move_robot(self, delta_x, delta_y):
        delta = rotate_vector(- self._robot_angle, Position(delta_x, delta_y))
        self.set_robot_position(self._robot_position.x + delta[0], self._robot_position.y + delta[1])

    def rotate_robot(self, angle):
        self._robot_angle += angle
        self._robot_angle = self._robot_angle % 360

