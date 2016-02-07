
class Robot():
    def __init__(self, wheels):
        self.__wheels = wheels

    def start(self):
        self.__wheels.start()

    def stop(self):
        self.__wheels.stop()

    def set_velocity(self, x_velocity, y_velocity):
        self.__wheels.set_velocity(x_velocity, y_velocity)

    def getpos(self):
        return self.__wheels.getpos()
