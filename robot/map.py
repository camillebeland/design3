import numpy as np
from utils.position import Position

class Map:
    def __init__(self, vision_daemon, worldmap_service, table_calibration_service):
        self.vision_daemon = vision_daemon
        self.worldmap_service = worldmap_service
        self.table_calibration_service = table_calibration_service

    def get_robot_position(self):
        return self.vision_daemon.get_robot_position_from_vision()

    def get_robot_angle(self):
        return self.vision_daemon.get_robot_angle_from_vision() % 360

    def relative_position(self, position):
        robot_current_position = self.get_robot_position()
        matrix = rotate_vector(self.get_robot_angle(), np.array(position.to_tuple()) - np.array(robot_current_position.to_tuple()))
        return Position(matrix[0], matrix[1])

    def add_treasures(self, treasures):
        self.worldmap_service.add_treasures(treasures)

    def get_recharge_station_position(self):
        position = self.worldmap_service.get_charging_station_position()
        charging_station_position = Position(position["x"], position["y"])
        return charging_station_position

    def get_table_corners(self):
        return self.table_calibration_service.get_table_corners()

    def get_treasure_closest_to(self, position):
        #TODO
        pass

    def find_island_with_clue(self, clue):
        islands = self.worldmap_service.get_islands()
        target_islands = list(filter(lambda island: self.filter_by_clue(island, clue), islands))
        target_island = target_islands.pop()
        return Position(target_island['x'], target_island['y'])

    def filter_by_clue(self, island, clue):
        if 'color' in clue.keys():
            return island['color'] == clue['color']
        elif 'shape' in clue.keys():
            return island['shape'] == clue['shape']
        else:
            return False


def rotate_vector(theta, vector):
    return np.dot(rotation_matrix(theta), vector)


def cos(angle):
    return np.cos(angle/180 * np.pi)


def sin(angle):
    return np.sin(angle/180 * np.pi)


def rotation_matrix(theta):
    return np.array([[cos(theta), -1*sin(theta)], [sin(theta), cos(theta)]])
