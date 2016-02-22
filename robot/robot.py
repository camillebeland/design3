from time import sleep
from threading import Thread
import math

class Robot():
    def __init__(self, wheels, worldmap, pathfinder):
        self.__wheels = wheels
        self.__worldmap = worldmap
        self.__pathfinder = pathfinder

    def move(self, delta_x, delta_y):
        self.__wheels.move(delta_x, delta_y)

    def getangle(self):
        return self.__worldmap.get_robot_angle()

    def getpos(self):
        return self.__worldmap.get_robot_position()

    def get_angle(self):
        return self.__worldmap.get_robot_angle()

    def move_to(self, final_destination):
        thread = Thread(target = self.move_to_thread, args= (final_destination,))
        thread.start()

    def move_to_thread(self, final_destination):
        while(distance(self.getpos(), final_destination) > 1):
            #sense
            position = self.getpos()
            #compute
            path = self.__pathfinder.find_path(position, final_destination)
            target = self.find_relative_target(path)
            #control
            self.__wheels.move(target[0], target[1])

            sleep(0.1)


    def rotate(self, angle):
        self.__wheels.rotate(angle)

    def find_relative_target(self, path):
        if(len(path) == 1):
            return self.__worldmap.relative_position(path[0])
        else:
            return self.__worldmap.relative_position(path[1])


def distance(pos1, pos2):
    x1,y1 = pos1
    x2,y2 = pos2
    return math.sqrt((x2-x1)**2 + (y2-y1)**2)
