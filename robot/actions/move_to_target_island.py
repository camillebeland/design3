from robot.action import Action
from utils.position import Position


class MoveToTargetIslandAction(Action):
    def start(self):
        self.running = True
        print('Moving to Target Island')
        self.island_position = self._context.robot.get_target_island_position()
        self._context.robot.move_to_target(self.island_position, self.path_done)

    def path_done(self):
        self._context.robot.rotate_towards(self.island_position, self.rotate_done)

    def rotate_done(self):
        if self.running:
            self._context.event_listener.notify_event(self._end_message)
        self.running = False

    def stop(self):
        print("Move to target island asked to stop")
        self._context.robot.stop()
        self.running = False

