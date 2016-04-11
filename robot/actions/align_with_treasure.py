from robot.action import Action
from robot.align_movement import AlignMovement
from robot.vision.treasure_position_deamon import TreasurePositionDeamon
import time


class AlignWithTreasureAction(Action):
    def start(self):
        treasures_position_deamon = TreasurePositionDeamon(self._context.embedded_camera)
        print(treasures_position_deamon)
        align_movement = AlignMovement(treasures_position_deamon, self._context.robot, align_move_distance=1,
                                       min_distance_to_target=2, marker_position_x=870, time_sleep=0.20)
        self._context.robot.set_camera_angle(25, 0)
        time.sleep(2)
        try:
            align_movement.start(self.__align_done)
        except Exception as e:
            print(e)

    def __align_done(self):
        self._context.robot.set_camera_angle(90, 0)
        self._context.robot.move(130, 0)
        time.sleep(2)
        self._context.event_listener.notify_event(self._end_message)