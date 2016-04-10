from robot.action import Action


class FindIslandClue(Action):
    def start(self):
        print('Finding Island Clue')
        code = self._context.robot.get_manchester_code()
        island_clue = self._context.robot_service.ask_target_island(code)
        print(island_clue)
        self._context.robot.set_island_clue(island_clue)
        self._context.event_listener.notify_event(self._end_message)

    def stop(self):
        raise NotImplementedError
