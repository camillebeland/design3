from robot.action import Action
import time


class MoveToChargeStationAction(Action):

    def start(self):
        self.running = True
        print('Moving To Charge Station')
        self._context.timer.start()
        self._context.robot.lift_prehenseur_down()
        self.__facing_charge_station_angle = 270
        self.__recharge_station_position = self._context.worldmap.get_recharge_station_position()
        self._context.robot.move_to(self.__recharge_station_position, self.__rotate)

    def __rotate(self):
        robot_angle = self._context.worldmap.get_robot_angle()
        self._context.robot.rotate(self.__facing_charge_station_angle - robot_angle, self.__rotate_done)

    def __rotate_done(self):
        self._context.robot.move_to(self.__recharge_station_position, self.__move_to_done)

    def __move_to_done(self):
        self._context.robot.move(0, -100)
        time.sleep(3)
        self._context.robot.move(60, 0)
        time.sleep(2)
        if self.running:
            self._context.event_listener.notify_event(self._end_message)
        self.running = False



    def stop(self):
        print("move to charge station asked to stop")
        self._context.robot.stop()
        self.running = False

