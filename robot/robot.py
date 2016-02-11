class Robot():
    def __init__(self, wheels, worldmap):
        self.__wheels = wheels
        self.__worldmap = worldmap

    def start(self):
        self.__wheels.start()

    def stop(self):
        self.__wheels.stop()

    def move(self, delta_x, delta_y):
        self.__wheels.move(delta_x, delta_y)

    def getpos(self):
        return self.__worldmap.get_robot_position()

    def rotate(self, angle):
        print("BOB")
        self.__wheels.rotate(angle)