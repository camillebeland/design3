from robot.action import Action


class MoveToChargeStationAction(Action):
    def __init__(self, robot, robot_service, worldmap, embedded_camera, charge_station_angle=-90):
        super().__init__(robot, robot_service, worldmap, embedded_camera)
        self.__charge_station_angle = charge_station_angle

    def start(self):
        recharge_station_position = self._worldmap.get_recharge_station_position()
        self._robot.move_to(recharge_station_position, self.__rotate)

    def __rotate(self):
        robot_angle = self._worldmap.get_robot_angle()
        self._robot.rotate(self.__charge_station_angle - robot_angle)

    def stop():
        #TODO
        raise NotImplementedError()
