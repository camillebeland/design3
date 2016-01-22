from threading import Thread
from time import sleep, clock

class Robot:
    def __init__ (self, refresh_time = 10):
        self.pos = [0,0]
        self.vel = [0,0]
        self.refresh_time = refresh_time
        
    def __update(self, refresh_time):
        print("Starting Thread for time simulation")
        while(self.running):
            time = clock()
            sleep(refresh_time/1000)
            time = clock() - time
            self.pos[0] += self.vel[0] * time
            self.pos[1] += self.vel[1] * time


    def __del__(self):
        self.running = False


    def start(self):
        self.thread = Thread(target = self.__update, args = (self.refresh_time, ))
        self.running = True
        self.thread.setDaemon(True)
        self.thread.start()


    def set_vel(self, vel_x, vel_y):
        self.vel[0] = vel_x
        self.vel[1] = vel_y


    def move(self, direction, speed):
        if(direction == 1):
            self.pos = [self.pos[0] - ticks, self.pos[1]]
