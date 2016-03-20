from robot.action_machine import Action

class MoveToTargetIslandAction(Action):
    def start(self):
        island_position = self._robot.get_target_island_position()
        self._robot.move_to(island_position)
