from robot.action import Action


class MoveToTargetIslandAction(Action):
    def start(self):
        print('Moving to Target Island')
        island_position = self._context.robot.get_target_island_position()
        self._context.robot.move_to(island_position, self.move_done)

    def move_done(self):
        self._context.event_listener.notify_event(self._end_message)
