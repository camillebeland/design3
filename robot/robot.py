from threading import Thread
from time import sleep
from math import cos, sin

class Mock_Robot:
    def __init__ (self, refresh_time = 10):
        self.pos = [0,0]
        self.vel = [0,0]
        self.refresh_time = refresh_time

    def __update(self, refresh_time):
        print("Starting Thread for time simulation")
        while(self.running):
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
        
    def set_vel(self, vel_x, vel_y):
        self.vel[0] = vel_x
        self.vel[1] = vel_y


    def move(self, angle, speed):
        self.vel[0] = cos(angle)*speed
        self.vel[1] = sin(angle)*speed
