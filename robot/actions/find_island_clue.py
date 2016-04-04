from robot.action import Action


class FindIslandClue(Action):
    def start(self):
        code = self._robot.get_manchester_code()
        island_clue = self._robot_service.ask_target_island(code)
        self._robot.set_island_clue(island_clue)
