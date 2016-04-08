from robot.action import Action
from robot.align_movement import AlignMovement
from robot.vision.treasure_position_deamon import TreasurePositionDeamon
import time

class AlignWithTreasureAction(Action):
    def start(self):
        charging_station_position_deamon = TreasurePositionDeamon(self._context.embedded_camera)
        # TODO find treasure align parameters
        align_movement = AlignMovement(charging_station_position_deamon, self._context.robot, align_move_distance=3,
                                       min_distance_to_target=15, marker_position_x=1215, time_sleep=1)
        self._context.robot.set_camera_angle(25, 0)
        time.sleep(2)
        try:
            align_movement.start(self.__align_done)
        except Exception as e:
            print(e)

    def __align_done(self):
        self._context.robot.move(30, 0)
