from robot.action import Action
from utils.position import Position


class MoveToTreasureAction(Action):
    def start(self):
        print('Moving to Treasure')
        self.treasure_position = self._context.robot.get_target_treasure_position()
        print(self.treasure_position)
        try:
            self._context.robot.move_to_target(self.treasure_position, self.path_done)
        except Exception as error:
            print(error) 

    def path_done(self):
        self._context.robot.rotate_towards(self.treasure_position, self.rotate_done)

    def rotate_done(self):
        self._context.event_listener.notify_event(self._end_message)

    def stop(self):
        raise NotImplementedError
