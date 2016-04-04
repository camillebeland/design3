from robot.action import Action
from time import sleep


class PickUpTreasure(Action):
    def start(self):
        self._robot.lift_prehenseur_down()
        sleep(1)
        self._robot.activate_magnet()
        sleep(0.2)
        self._robot.move(-15, 0)
        sleep(2)
        self._robot.lift_prehenseur_up()
        sleep(1)
        self._robot.deactivate_magnet()
