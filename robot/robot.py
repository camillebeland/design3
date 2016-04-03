class Robot:

    def __init__(self, wheels, world_map, pathfinder, manchester_antenna, movement, battery, magnet):
        self.__wheels = wheels
        self.__world_map = world_map
        self.__movement = movement
        self.__manchester_antenna = manchester_antenna
        self.__battery = battery
        self.__magnet = magnet
        self.__manchester_code = ''
        self.__island_clue = ''

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

    def set_manchester_code(self, code):
        self.__manchester_code = code

    def change_target_island_position(self, island_position):
        self.__island_position = island_position

    def get_target_island_position(self):
        return self.__island_position

    def change_target_treasure_position(self, treasure_position):
        self.__treasure_position = treasure_position

    def get_target_treasure_position(self):
        return self.__treasure_position

    def get_battery_level(self):
        return self.__battery.get_level()

    def get_capacitor_charge(self):
        return self.__magnet.get_charge()

    def get_path(self):
        return self.__movement.get_last_path_used()

    def move_to(self, final_destination, callback):
        self.__movement.move_to(final_destination, callback)

    def find_move_to(self, position):
        #TODO
        pass

    def rotate(self, angle):
        self.__wheels.rotate(angle)

    def stop(self):
        self.__movement.stop_any_movement()
        self.__wheels.stop()

    def activate_magnet(self):
        self.__magnet.activate()

    def deactivate_magnet(self):
        self.__magnet.deactivate()

    def lift_prehenseur_up(self):
        self.__magnet.lift_up()

    def lift_prehenseur_down(self):
        self.__magnet.lift_down()

    def get_island_clue(self):
        return self.__island_clue

    def recharge_magnet(self, callback):
        self.__magnet.recharge(callback)

    def set_island_clue(self, clue):
        self.__island_clue = clue
