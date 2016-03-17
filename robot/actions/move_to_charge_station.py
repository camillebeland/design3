
class MoveToChargeStationAction:
    def __init__(self, robot, worldmap, action_machine):
        self.__robot = robot
        self.__worldmap = worldmap
        self.__action_machine = action_machine
        self.__charge_station_angle = 0

    def start():
        recharge_station_position = self.__worldmap.get_recharge_station_position()
        self.__robot.move_to(recharge_station_position)
        robot_angle = self.__worldmap.get_robot_angle()
        self.__robot.rotate(self.__charge_station_angle - robot_angle)
        self.__action_machine.notify_event('charge')

    def stop():
        pass
