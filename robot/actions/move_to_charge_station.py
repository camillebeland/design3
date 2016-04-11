from robot.action import Action


class MoveToChargeStationAction(Action):

    def start(self):
        print('Moving To Charge Station')
        self._context.robot.lift_prehenseur_down()
        self.__facing_charge_station_angle = 270
        recharge_station_position = self._context.worldmap.get_recharge_station_position()
        self._context.robot.move_to(recharge_station_position, self.__rotate)

    def __rotate(self):
        robot_angle = self._context.worldmap.get_robot_angle()
        self._context.robot.rotate(self.__facing_charge_station_angle - robot_angle, self.__rotate_done)

    def __rotate_done(self):
        self._context.event_listener.notify_event(self._end_message)

    def stop(self):
        #TODO
        raise NotImplementedError()
