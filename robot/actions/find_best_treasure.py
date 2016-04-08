from robot.action import Action

class FindBestTreasureAction(Action):
    def start(self):
        print('Finding Best Treasure')
        robot_position = self._context.robot.get_position()
        target_island_position = self._context.robot.get_target_island_position()
        treasure_position = self._context.treasure_easiest_path.find_easiest_treasure_from(robot_position, target_island_position)
        print(treasure_position.to_tuple())
        self._context.robot.change_target_treasure_position(treasure_position)
        self._context.event_listener.notify_event(self._end_message)

    def stop(self):
        raise NotImplementedError
