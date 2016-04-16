import math
from threading import Thread
from time import sleep

from robot.errors.no_connection_exception import NoConnectionException
from utils.math import rotate_vector
from utils.position import Position


class Movement:
    def __init__(self, compute, sense, control, loop_time=5, min_distance_to_destination=40):
        self.__compute = compute
        self.__sense = sense
        self.__control = control
        self.__should_move = False
        self.__loop_time = loop_time
        self.__min_distance_to_destination = min_distance_to_destination
        self.__min_distance_to_target = 250
        self.__current_path = list()

    def init_vision(self, pathfinder):
        self.__compute = pathfinder

    def get_last_path_used(self):
        return self.__current_path

    def move_to(self, final_destination, callback=None):
        if self.__compute is not None:
            self.__should_move = False
            sleep(self.__loop_time)
            self.__thread = Thread(target=self.move_to_thread, args=(final_destination, callback))
            self.__should_move = True
            self.__thread.start()
        else:
            print('Need to initialize vision')

    def move_to_thread(self, final_destination, callback):
        while self.__should_move and self.__not_close_enough_to_destination(final_destination):
            sleep(self.__loop_time)
            # sense
            try:
                self.__actual_position = self.__sense.get_robot_position()
                print(self.__actual_position)
            except Exception as exception:
                print(exception)
                continue
            self.__actual_position = self.__sense.get_robot_position()
            self.__actual_robot_angle = self.__sense.get_robot_angle()
            # compute
            self.__current_path = self.__compute.find_path(self.__actual_position, final_destination)
            target = self.find_relative_target(self.__current_path)
            # control
            self.__control.move(target.x, target.y)

        if callback is not None:
            callback()
        self.__current_path = list()

    def __not_close_enough_to_destination(self, destination):
        try:
            self.__actual_distance = distance_between(self.__sense.get_robot_position(), destination)
            return self.__actual_distance > self.__min_distance_to_destination
        except NoConnectionException as exception:
            print('(Ignored) : ',exception)
            return True

    def find_relative_target(self, path):
        if len(path) is 0:
            self.__should_move = False
            return 0, 0
        elif len(path) is 1:
            return self._relative_position(path[0])
        else:
            return self._relative_position(path[1])

    def move_to_target(self, target, callback):
        if self.__compute is not None:
            self.__should_move = False
            sleep(self.__loop_time)
            self.__thread = Thread(target=self.move_to_target_thread, args=(target, callback))
            self.__should_move = True
            self.__thread.start()
        else:
            print('Need to initialize vision')

    def move_to_target_thread(self, target, callback):
        while self.__should_move and self.__not_close_enough_to_target(target):
            sleep(self.__loop_time)
            # sense
            try:
                self.__actual_position = self.__sense.get_robot_position()
            except NoConnectionException as exception:
                print(exception)
                continue
            self.__actual_robot_angle = self.__sense.get_robot_angle()
            # compute
            self.__current_path = self.__compute.find_path(self.__actual_position, target)
            relative_target = self.find_relative_target(self.__current_path)
            # control
            self.__control.move(relative_target.x, relative_target.y)
        self.stop_any_movement()
        if callback is not None:
            callback()
        self.__current_path = list()

    def __not_close_enough_to_target(self, target):
        try:
            self.__actual_distance = distance_between(self.__sense.get_robot_position(), target)
            return self.__actual_distance > self.__min_distance_to_target
        except NoConnectionException as exception:
            print('(Ignored) : ', exception)
            return True

    def stop_any_movement(self):
        self.__should_move = False
        self.__control.close_connection()

    def _relative_position(self, position):
        matrix = rotate_vector(self.__actual_robot_angle, position - self.__actual_position)
        return Position(matrix[0], matrix[1])

    def change_path_finder(self, pathfinder):
        self.__compute = pathfinder


def distance_between(position1, position2):
    x1 = position1.x
    y1 = position1.y
    x2 = position2.x
    y2 = position2.y
    euclidean_distance = math.sqrt((x2-x1)**2 + (y2-y1)**2)
    return euclidean_distance
