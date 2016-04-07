from time import sleep
from threading import Thread
import math
from utils.math import rotate_vector


class AlignMovement:
    def __init__(self, position_deamon, robot, align_move_distance=30, min_distance_to_target=20):
        self.__robot = robot
        self.__position_deamon = position_deamon
        self.__align_move_distance = align_move_distance
        self.__min_distance_to_target = min_distance_to_target

    def init_vision(self):
        self.__position_deamon.start_fetching_treasure_position_from_vision()

    def start(self):
        move_direction = self.compute_move_direction()
        self.__robot.move(move_direction)
        self.align()

    def align(self, callback=None):
        self.__thread = Thread(target=self.align_thread, args=(callback,))
        self.__thread.start()

    def align_thread(self, callback):
        target = self.__position_deamon.get_position_from_vision[0]
        while not self.__close_enough_to_target(target):
            target = self.__position_deamon.get_position_from_vision[0]
        self.stop_any_movement()
        if callback is not None:
            callback()

    def __close_enough_to_target(self, target):
        if -self.__min_distance_to_target < target < self.__min_distance_to_target:
            return True
        else:
            return False

    def stop_any_movement(self):
        self.__robot.stop()

    def compute_move_direction(self):
        if self.__position_deamon.get_position_from_vision[0] > 800:
            return -self.__align_move_distance
        else:
            return self.__align_move_distance
