class Robot:

    def __init__(self, wheels, world_map, pathfinder, manchester_antenna, movement, battery):
        self.__wheels = wheels
        self.__world_map = world_map
        self.__movement = movement
        self.__manchester_antenna = manchester_antenna
        self.__battery = battery

    def move(self, delta_x, delta_y):
        self.__wheels.move(delta_x, delta_y)

    def get_position(self):
        return self.__world_map.get_robot_position()

    def get_angle(self):
        return self.__world_map.get_robot_angle()

    def get_battery_level(self):
        return self.__battery.get_level()

    def get_capacitor_charge(self):
        return self.__manchester_antenna.get_capacitor_charge()

    def get_manchester_code(self):
        return self.__arduino.get_manchester_code()

    def get_path(self):
        return self.__movement.get_last_path_used()

    def move_to(self, final_destination):
        self.__movement.move_to(final_destination)

    def rotate(self, angle):
        self.__wheels.rotate(angle)
