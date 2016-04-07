from robot.action import Action


class MoveToTreasureAction(Action):
    def start(self):
        print('Moving to Treasure')
        treasure_position = self._context.robot.get_target_treasure_position()
        self._context.robot.move_to_target(treasure_position, self.move_done)

    def move_done(self):
        self._context.event_listener.notify_event(self._end_message)

    def stop(self):
        raise NotImplementedError
