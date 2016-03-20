from robot.action_machine import Action

class MoveToTreasureAction(Action):
    def start(self):
        treasure_position = self.__robot.get_target_treasure_position()
        self.__robot.move_to(treasure_position)
