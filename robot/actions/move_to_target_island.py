from robot.action import Action


class MoveToTargetIslandAction(Action):
    def start(self):
        print('Moving to Target Island')
        self.island_position = self._context.robot.get_target_island_position()
        self._context.robot.move_to_target(self.island_position, self.path_done)

    def path_done(self):
        self._context.robot.rotate_towards(self.island_position, self.rotate_done)

    def rotate_done(self):
        self._context.event_listener.notify_event(self._end_message)

    def stop(self):
        raise NotImplementedError
