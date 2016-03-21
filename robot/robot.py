from robot.movement import Movement


class Robot:
    def __init__(self, wheels, world_map, pathfinder, http_service, arduino, magnet):
        self.__wheels = wheels
        self.__world_map = world_map
        self.__movement = Movement(pathfinder, world_map, wheels, http_service)
        self.__arduino = arduino
        self.__magnet = magnet

    def move(self, delta_x, delta_y):
        self.__wheels.move(delta_x, delta_y)

    def get_position(self):
        return self.__world_map.get_robot_position()

    def get_angle(self):
        return self.__world_map.get_robot_angle()

    def get_battery_level(self):
        return self.__arduino.get_battery_level()

    def get_capacitor_charge(self):
        return self.__arduino.get_capacitor_charge()

    def get_manchester_code(self):
        return self.__arduino.get_manchester_code()

    def get_path(self):
        return self.__movement.get_last_path_used()

    def move_to(self, final_destination):
        self.__movement.move_to(final_destination)

    def rotate(self, angle):
        self.__wheels.rotate(angle)

    def set_mock_movement(self, mock_movement):
        self.__movement = mock_movement

    def activate_magnet(self):
        self.__magnet.activate()
