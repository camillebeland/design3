from robot.action import Action


class PickUpTreasure(Action):
    def start(self):
        self._robot.activate_magnet()
