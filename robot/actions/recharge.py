from robot.action import Action
from time import sleep

class RechargeAction(Action):
    def start(self):
        self._robot.start_recharge_magnet()
        while(self._robot.get_capacitor_charge() < 90.0):
            print(self._robot.get_capacitor_charge())
            sleep(1)
        self._robot.stop_recharge_magnet()
