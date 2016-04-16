from robot.action import Action
from utils.position import Position
from math import cos, sin, pi
import time

class MoveToTreasureAction(Action):
    def start(self):
        self.running = True
        print('Moving to Treasure')
        self.treasure_position = self._context.robot.get_target_treasure_position()
        self.facing_angle = self.__find_facing_angle_when_upfront(self.treasure_position, self._context.worldmap.table_calibration_service.get_table_corners())
        wall_distance = 180
        position_ajustment = Position(-cos(2*pi*self.facing_angle/360.0), sin(2*pi*self.facing_angle/360.0)) * wall_distance
        print(self.facing_angle, position_ajustment)
        try:
            self._context.robot.move_to(self.treasure_position + position_ajustment, self.path_done)
        except Exception as error:
            print(error) 

    def path_done(self):
        self.rotate_towards_treasure(self.rotate_done)

    def rotate_done(self):
        self._context.robot.lift_prehenseur_down()
        time.sleep(0.5)
        if self.running:
            self._context.event_listener.notify_event(self._end_message)
        self.running = False

    def rotate_towards_treasure(self, callback=None):
        self._context.robot.rotate_to(self.facing_angle, callback)

    def __find_facing_angle_when_upfront(self, treasure_position, table_corners):
        facing_angle = None
        gripper_offset = 270
        tolerance = 100
        approximated_left_limit = table_corners[0][0]
        approximated_top_limit = table_corners[2][1]
        approximated_bottom_limit = table_corners[0][1]

        if (approximated_bottom_limit - tolerance) <= treasure_position.y < (approximated_bottom_limit + tolerance):
            facing_angle = 180
        elif (approximated_left_limit - tolerance) <= treasure_position.x < (approximated_left_limit + tolerance):
            facing_angle = 270
        elif (approximated_top_limit - tolerance) <= treasure_position.y < (approximated_top_limit + tolerance):
            facing_angle = 0
        elif facing_angle is None:
            facing_angle = 180

        return facing_angle + gripper_offset

    def stop(self):
        print("Move to treasure asked to stop")
        self._context.robot.stop()
        self.running = False

