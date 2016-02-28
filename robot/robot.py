from robot.movement import Movement

class Robot():
    def __init__(self, wheels, worldmap, pathfinder):
        self.__wheels = wheels
        self.__worldmap = worldmap
        self.__movement = Movement(pathfinder, worldmap, wheels)

    def move(self, delta_x, delta_y):
        self.__wheels.move(delta_x, delta_y)

    def get_position(self):
        return self.__worldmap.get_robot_position()

    def get_angle(self):
        return self.__worldmap.get_robot_angle()

    def move_to(self, final_destination):
        self.__movement.move_to(final_destination)

    def rotate(self, angle):
        self.__wheels.rotate(angle)

