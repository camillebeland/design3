
class Robot():
    def __init__(self, wheels):
        self.__wheels = wheels

    def start(self):
        self.__wheels.start()

    def stop(self):
        self.__wheels.stop()

    def set_velolicty(self, vel_x, vel_y):
        self.__wheels.vel[0] = vel_x
        self.__wheels.vel[1] = vel_y

    def move(self, angle, speed):
        self.__wheels.vel[0] = cos(angle)*speed
        self.__wheels.vel[1] = sin(angle)*speed

    def getpos(self):
        return self.__wheels.getpos()
