from robot.action import Action
from time import sleep

class PickUpTreasure(Action):
    def start(self):
        self._robot.lift_prehenseur_down()
        sleep(1)
        self._robot.activate_magnet()
        self._robot.lift_prehenseur_up()
        sleep(1)
        self._robot.deactivate_magnet()
