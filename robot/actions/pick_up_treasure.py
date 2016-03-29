from robot.action import Action


class PickUpTreasure(Action):
    def start(self, robot):
        robot.activate_magnet()
