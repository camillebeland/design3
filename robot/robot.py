class Robot():
    def __init__(self, wheels, worldmap):
        self.__wheels = wheels
        self.__worldmap = worldmap

    def move(self, delta_x, delta_y):
        self.__wheels.move(delta_x, delta_y)

    def getpos(self):
        return self.__worldmap.get_robot_position()

    def get_angle(self):
        return self.__worldmap.get_robot_angle()

    def rotate(self, angle):
        self.__wheels.rotate(angle)
