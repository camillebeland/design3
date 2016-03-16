from threading import Thread
from time import sleep
from math import cos, sin, pow, sqrt

PRECISION = 0.00001


class SimulationWheels:
    def __init__ (self, worldmap, wheels_velocity=5, refresh_time = 10):
        self.refresh_time = refresh_time
        self.running = False
        self.worldmap = worldmap
        self.wheels_velocity= wheels_velocity
        self.target = [0,0]
        self.direction = [0,0]

        self.thread = Thread(target = self.__update, args = (self.refresh_time, ))
        self.running = True
        self.thread.setDaemon(True)
        self.thread.start()


    def __update(self, refresh_time):
        while self.running:
            sleep(refresh_time/1000)
            delta_x = self.wheels_velocity * self.direction[0] * refresh_time/1000
            delta_y = self.wheels_velocity * self.direction[1] * refresh_time/1000

            if(self.target[0]*self.direction[0] < PRECISION
               and self.target[1]*self.direction[1] < PRECISION):
                delta_x = self.target[0]
                delta_y = self.target[1]
                self.direction = [0,0]

            self.worldmap.move_robot(delta_x, delta_y)
            self.target[0] -= delta_x
            self.target[1] -= delta_y


    def __del__(self):
        self.running = False

    def move(self, x_pos, y_pos):
        self.target[0] = x_pos
        self.target[1] = y_pos

        length = sqrt(pow(self.target[0], 2) + pow(self.target[1], 2))

        if(length < PRECISION):
            self.direction[0] = 0
            self.direction[1] = 0
        else:
            self.direction[0] = self.target[0] / length
            self.direction[1] = self.target[1] / length


    def rotate(self, angle):
        self.worldmap.rotate_robot(angle)

