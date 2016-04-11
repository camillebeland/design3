from robot.action import Action


class FindIslandClue(Action):
    def start(self):
        self.running = True
        print('Finding Island Clue')
        code = self._context.robot.get_manchester_code()
        island_clue = self._context.robot_service.ask_target_island(code)
        print(island_clue)
        self._context.robot.set_island_clue(island_clue)
        if self.running:
            self._context.event_listener.notify_event(self._end_message)
        self.running = False

    def stop(self):
        print("Find island clue asked to stop")
        self.running = False

