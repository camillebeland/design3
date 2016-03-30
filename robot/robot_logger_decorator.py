class RobotLoggerDecorator:
    def __init__(self, robot, logger_service):
        self.__robot = robot
        self.__logger_service = logger_service

    def move(self, delta_x, delta_y):
        # TODO fix logger
        # self.__logger_service.log_info('Robot Move ({0},{1})'.format(delta_x, delta_y))
        self.__robot.move(delta_x, delta_y)

    def get_position(self):
        return self.__robot.get_position()

    def get_angle(self):
        return self.__robot.get_angle()

    def get_battery_level(self):
        return self.__robot.get_battery_level()

    def get_capacitor_charge(self):
        return self.__robot.get_capacitor_charge()

    def find_manchester_code(self):
        self.__logger_service.log_info('Robot Finding Manchester code')
        self.__robot.find_manchester_code()

    def get_manchester_code(self):
        return self.__robot.get_manchester_code()

    def set_manchester_code(self, code):
        self.__logger_service.log_info('Robot Setting Manchester Code to {0}'.format(code))
        return self.__robot.set_manchester_code(code)

    def get_path(self):
        return self.__robot.get_path()

    def move_to(self, final_destination):
        #self.__logger_service.log_info('Robot Move_to {0}'.format(final_destination))
        self.__robot.move_to(final_destination)

    def rotate(self, angle):
        self.__logger_service.log_info('Robot Rotate {0}'.format(angle))
        self.__robot.rotate(angle)

    def stop(self):
        self.__logger_service.log_info("Robot asked to stop it's current path")
        self.__robot.stop()
