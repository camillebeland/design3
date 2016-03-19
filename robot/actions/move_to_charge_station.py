
class MoveToChargeStationAction:
    def __init__(self, robot, worldmap, charge_station_angle=90):
        self.__robot = robot
        self.__worldmap = worldmap

        self.__charge_station_angle = charge_station_angle

    def start(self):
       print('Moving to charge station')
       recharge_station_position = self.__worldmap.get_recharge_station_position()
       self.__robot.move_to(recharge_station_position)
       robot_angle = self.__worldmap.get_robot_angle()
       self.__robot.rotate(self.__charge_station_angle - robot_angle)

    def stop():
        #TODO
        raise NotImplementedError()
