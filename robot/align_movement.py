import time
from threading import Thread


class AlignMovement:
    def __init__(self, position_deamon, robot, align_move_distance=3, min_distance_to_target=15, marker_position_x=1215, time_sleep=1):
        self.__robot = robot
        self.__position_deamon = position_deamon
        self.__align_move_distance = align_move_distance
        self.__min_distance_to_target = min_distance_to_target
        self.__marker_position_x = marker_position_x
        self.__time_sleep = time_sleep
        self.move_distance = 0

    def __init_vision__(self):
        self.__position_deamon.start_fetching_position_from_vision()

    def start(self, callback):
        self.__init_vision__()
        self.__align__(callback)

    def __align__(self, callback=None):
        self.__thread = Thread(target=self.__align_thread__, args=(callback,))
        self.__thread.start()
        self.__move_thread = Thread(target=self.__move_thread__, args=(self.__time_sleep,))
        self.should_move = True
        self.__move_thread.start()

    def __align_thread__(self, callback):
        is_aligned = False
        while not is_aligned:
            target_x = self.__position_deamon.get_position_from_vision()[0]
            if target_x is 0:
                continue
            self.move_distance = self.__compute_move_direction__(target_x)
            if self.__close_enough_to_target__(target_x):
                self.should_move = False
                self.__stop_any_movement__()
                is_aligned = True
        if callback is not None:
            callback()

    def __move_thread__(self, time_sleep):
        print("movebefore")
        while self.should_move:
            print("move")
            self.__robot.move(0, self.move_distance)
            time.sleep(time_sleep)

    def __close_enough_to_target__(self, target):
        if (self.__marker_position_x - self.__min_distance_to_target) < target < (self.__marker_position_x + self.__min_distance_to_target):
            return True
        else:
            return False

    def __stop_any_movement__(self):
        self.__robot.stop()

    def __compute_move_direction__(self, target_x):
        if target_x is 0:
            return 0
        if target_x > self.__marker_position_x:
            return -self.__align_move_distance
        else:
            return self.__align_move_distance
