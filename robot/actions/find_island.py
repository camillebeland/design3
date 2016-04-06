from robot.action import Action


class FindIslandAction(Action):
    def start(self):
        print('Finding Island')
        island_clue = self._context.robot.get_island_clue
        island_position = self._context.worldmap.find_island_with_clue(island_clue)
        self._context.robot.change_target_island_position(island_position)
        self._context.event_listener.notify_event(self._end_message)

    def stop(self):
        raise NotImplementedError
