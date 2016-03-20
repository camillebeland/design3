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

    def find_manchester_code(self):
        self.__manchester_code = self.__manchester_antenna.get_manchester_code()

    def get_manchester_code(self):
        return self.__manchester_code

    def change_target_island_position(self, island_position):
        self.__island_position = island_position

    def get_target_island_position(self):
        return self.__island_position

    def change_target_treasure_position(self, treasure_position):
        self.__treasure_position = treasure_position

    def get_target_treasure_position(self):
        return self.__treasure_position

    def get_path(self):
        return self.__movement.get_last_path_used()

    def move_to(self, final_destination):
        self.__movement.move_to(final_destination)

    def find_move_to(self, position):
        #TODO
        pass

    def rotate(self, angle):
        self.__wheels.rotate(angle)

    def set_mock_movement(self, mock_movement):
        self.__movement = mock_movement

