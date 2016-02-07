from threading import Thread
from time import sleep
from math import cos, sin


class MockWheels:
    def __init__ (self, refresh_time = 10):
        print("Initiating MockWheels")
        self.pos = [0,0]
        self.vel = [0,0]
        self.refresh_time = refresh_time
        self.running = False

    def __update(self, refresh_time):
        print("Starting Thread for time simulation on MockWheels")
        while self.running:
            sleep(refresh_time/1000)
            self.pos[0] += self.vel[0] * refresh_time/1000
            self.pos[1] += self.vel[1] * refresh_time/1000


    def __del__(self):
        self.stop()

    def start(self):
        self.thread = Thread(target = self.__update, args = (self.refresh_time, ))
        self.running = True
        self.thread.setDaemon(True)
        self.thread.start()

    def stop(self):
        self.running = False

    def getpos(self):
        return self.pos

    def set_velocity(self, x_velocity, y_velocity):
        self.vel[0] = x_velocity
        self.vel[1] = y_velocity
