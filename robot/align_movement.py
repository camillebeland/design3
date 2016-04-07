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

    def __init_vision__(self):
        self.__position_deamon.start_fetching_position_from_vision()

    def start(self, callback):
        self.__init_vision__()
        move_direction = self.__compute_move_direction__()
        self.__robot.move(0, move_direction)
        self.__align__(callback)

    def __align__(self, callback=None):
        self.__thread = Thread(target=self.__align_thread__, args=(callback,))
        self.__thread.start()

    def __align_thread__(self, callback):
        target = self.__position_deamon.get_position_from_vision()[0]
        while not self.__close_enough_to_target__(target):
            target = self.__position_deamon.get_position_from_vision()[0]
        self.__stop_any_movement__()
        if callback is not None:
            callback()

    def __close_enough_to_target__(self, target):
        if -self.__min_distance_to_target < target < self.__min_distance_to_target:
            return True
        else:
            return False

    def __stop_any_movement__(self):
        self.__robot.stop()

    def __compute_move_direction__(self):
        position = self.__position_deamon.get_position_from_vision()
        print(position)
        print("position")
        if position[0] > 660:
            return self.__align_move_distance
        else:
            return -self.__align_move_distance
