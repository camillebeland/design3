from time import sleep
from threading import Thread
import math

class Movement:
    def __init__(self, compute, sense, control):
        self.__compute = compute
        self.__sense = sense
        self.__control = control
        self.__moving = False
        self.__loop_time = 1
        self.__distance = 20

    def move_to(self, final_destination):
        self.__moving = False
        sleep(self.__loop_time)
        self.__thread = Thread(target = self.move_to_thread, args= (final_destination,))
        self.__moving = True
        self.__thread.start()

    def move_to_thread(self, final_destination):
        while(self.__moving and distance(self.__sense.get_robot_position(), final_destination) > self.__distance):
            #sense
            position = self.__sense.get_robot_position()
            #compute
            path = self.__compute.find_path(position, final_destination)
            target = self.find_relative_target(path)
            #control
            self.__control.move(target[0], target[1])
            sleep(self.__loop_time)


    def find_relative_target(self, path):
        if(len(path) == 1):
            return self.__sense.relative_position(path[0])
        else:
            return self.__sense.relative_position(path[1])


def distance(pos1, pos2):
    x1,y1 = pos1
    x2,y2 = pos2
    return math.sqrt((x2-x1)**2 + (y2-y1)**2)

