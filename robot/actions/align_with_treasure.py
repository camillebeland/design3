from robot.action import Action
from robot.align_movement import AlignMovement
from robot.vision.treasure_position_deamon import TreasurePositionDeamon
import time


class AlignWithTreasureAction(Action):
    def start(self):
        self.running = True
        treasures_position_deamon = TreasurePositionDeamon(self._context.embedded_camera)
        print(treasures_position_deamon)
        # TODO find treasure align parameters
        align_movement = AlignMovement(treasures_position_deamon, self._context.robot, align_move_distance=3,
                                       min_distance_to_target=5, marker_position_x=905, time_sleep=1)
        self._context.robot.set_camera_angle(0, 0)
        time.sleep(2)
        try:
            align_movement.start(self.__align_done)
        except Exception as e:
            self.running = False
            print(e)

    def __align_done(self):
        self._context.robot.set_camera_angle(90, 0)
        self._context.robot.move(100, 0)
        if self.running:
            self._context.event_listener.notify_event(self._end_message)

    def stop(self):
        print("Align treasure asked to stop")
        self._context.robot.stop()
        self.running = False
