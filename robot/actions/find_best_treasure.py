from robot.action import Action

class FindBestTreasureAction(Action):
    def start(self):
        print('Finding Best Treasure')
        island_position = self._context.robot.get_target_island_position()
        treasure_position = self._context.worldmap.get_treasure_closest_to(island_position)
        self._context.robot.change_target_treasure_position(treasure_position)
        self._context.event_listener.notify_event(self._end_message)

    def stop(self):
        raise NotImplementedError
