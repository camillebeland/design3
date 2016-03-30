from robot.action import Action
from time import sleep

class RechargeAction(Action):
    def start(self):
        self.__robot.start_recharge_magnet()
        while(self.__robot.get_capacitor_charge < 90.0):
            sleep(1)
        self.__robot.stop_recharge_magnet()
