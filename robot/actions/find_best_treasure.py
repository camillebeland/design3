from robot.action import Action


class FindBestTreasureAction(Action):
    def start(self):
        island_position = self._robot.get_target_island_position()
        treasure_position = self._worldmap.get_treasure_closest_to(island_position)
        self._robot.change_target_treasure_position(treasure_position)
