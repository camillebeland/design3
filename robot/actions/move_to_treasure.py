from robot.action import Action


class MoveToTreasureAction(Action):
    def start(self):
        treasure_position = self._robot.get_target_treasure_position()
        self._robot.move_to(treasure_position)
