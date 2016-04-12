from robot.action import Action
from utils.position import Position
from math import cos, sin

class MoveToTreasureAction(Action):
    def start(self):
        self.running = True
        print('Moving to Treasure')
        self.treasure_position = self._context.robot.get_target_treasure_position()
        self.facing_angle = self.__find_facing_angle_when_upfront(self.treasure_position)
        wall_distance = 300
        position_ajustment = Position(-cos(self.facing_angle), sin(self.facing_angle)) * wall_distance
        try:
            self._context.robot.move_to(self.treasure_position + position_ajustment, self.path_done)
        except Exception as error:
            print(error) 

    def path_done(self):
        self._context.robot.rotate_towards_treasure(self.rotate_done)

    def rotate_done(self):
        if self.running:
            self._context.event_listener.notify_event(self._end_message)
        self.running = False

    def rotate_towards_treasure(self, callback=None):
        gripper_offset = 270
        self._context.rotate_to(self.facing_angle + gripper_offset, callback)

    def __find_facing_angle_when_upfront(self, treasure_position):
        facing_angle = None
        approximated_left_limit = 0
        approximated_top_limit = 975
        approximated_bottom_limit = 250

        if treasure_position.y < approximated_bottom_limit:
            facing_angle = 180
        elif treasure_position.x < approximated_left_limit:
            facing_angle = 270
        elif treasure_position.y > approximated_top_limit:
            facing_angle = 0
        elif facing_angle is None:
            facing_angle = 180
        return facing_angle

    def stop(self):
        print("Move to treasure asked to stop")
        self._context.robot.stop()
        self.running = False

