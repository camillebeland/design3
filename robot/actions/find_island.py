from robot.action_machine import Action

class FindIsland(Action):
    def start(self, ):
        code = self.__robot.get_manchester_code()
        island_clue = self.__robot_service.ask_target_island(code)
        island_position = self.__worldmap.find_island_with_clue(island_clue)
        self.__robot.change_target_island_position(island_position)
