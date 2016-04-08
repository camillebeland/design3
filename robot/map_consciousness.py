from time import time

from utils.dto.position import Position


class MapConsciousness:
    def __init__(self, actual_map, initial_position, initial_angle, distance_threshold=50):
        time_init = time()
        self.__robot_position = (time_init, initial_position)
        self.__robot_angle = (time_init, initial_angle)
        self.__velocity = Position(0,0)
        self.__map = actual_map
        self.__distance_threshold = distance_threshold

    def get_robot_position(self):
        timestamp = time()

def compute_velocity(new_position, old_position):
    return new_position[1].distance(old_position[1]) / (new_position[0] - old_position[0])
