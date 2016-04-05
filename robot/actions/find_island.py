from robot.action import Action


class FindIsland(Action):
    def start(self):
        island_clue = self._robot.get_island_clue
        island_position = self._worldmap.find_island_with_clue(island_clue)
        self._robot.change_target_island_position(island_position)

    def stop(self):
        raise NotImplementedError