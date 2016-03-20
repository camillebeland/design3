from robot.action_machine import Action

class FindBestTreasureAction(Action):
    def start(self):
        island_position = self.__robot.get_target_island_position()
        treasure_position = self.__worldmap.get_treasure_closest_to(island_position)
        self.__robot.change_target_treasure_position(treasure_position)
