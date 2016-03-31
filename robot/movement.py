from time import sleep
from threading import Thread
import math


class Movement:
    def __init__(self, compute, sense, control, loop_time=5, min_distance_to_target=40):
        self.__compute = compute
        self.__sense = sense
        self.__control = control
        self.__should_move = False
        self.__loop_time = loop_time
        self.__min_distance_to_target = min_distance_to_target
        self.__current_path = list()

    def get_last_path_used(self):
        return self.__current_path

    def move_to(self, final_destination, callback=None):
        self.__should_move = False
        sleep(self.__loop_time)
        self.__thread = Thread(target = self.move_to_thread, args= (final_destination, callback,))
        self.__should_move = True
        self.__thread.start()

    def move_to_thread(self, final_destination, callback):
        while self.__should_move and self.__not_close_enough_to_target(final_destination):
            # sense
            position = self.__sense.get_robot_position()
            # compute
            path = self.__compute.find_path(position, final_destination)
            self.__current_path = path
            target = self.find_relative_target(path)
            # control
            self.__control.move(target[0], target[1])
            sleep(self.__loop_time)
        if callback is not None:
            callback()
        self.__current_path = list()

    def __not_close_enough_to_target(self, target):
        actual_distance = distance_between(self.__sense.get_robot_position(), target)
        return actual_distance > self.__min_distance_to_target

    def find_relative_target(self, path):
        if len(path) == 1:
            return self.__sense.relative_position(path[0])
        else:
            return self.__sense.relative_position(path[1])

    def stop_any_movement(self):
        self.__should_move = False


def distance_between(position1, position2):
    x1 = position1.x
    y1 = position1.y
    x2 = position2.x
    y2 = position2.y
    euclidean_distance = math.sqrt((x2-x1)**2 + (y2-y1)**2)
    return euclidean_distance
