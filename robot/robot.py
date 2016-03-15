from robot.movement import Movement


class Robot:
    def __init__(self, wheels, world_map, pathfinder, http_service, manchester_antenna):
        self.__wheels = wheels
        self.__world_map = world_map
        self.__movement = Movement(pathfinder, world_map, wheels, http_service)
        self.__manchester_antenna = manchester_antenna

    def move(self, delta_x, delta_y):
        self.__wheels.move(delta_x, delta_y)

    def get_position(self):
        return self.__world_map.get_robot_position()

    def get_angle(self):
        return self.__world_map.get_robot_angle()

    def get_manchester_code(self):
        return self.__manchester_antenna.get_manchester_code()

    def move_to(self, final_destination):
        self.__movement.move_to(final_destination)

    def rotate(self, angle):
        self.__wheels.rotate(angle)

    def set_mock_movement(self, mock_movement):
        self.__movement = mock_movement

