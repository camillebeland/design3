from robot.action import Action
from robot.align_movement import AlignMovement
from robot.vision.charging_station_position_deamon import ChargingStationPositionDeamon
import time


class AlignWithChargingStationAction(Action):
    def start(self):
        self._context.robot.move(10, -180)
        time.sleep(3)
        self._context.robot.set_camera_angle(25, 0)
        time.sleep(2)
        try:
            charging_station_position_deamon = ChargingStationPositionDeamon(self._context.embedded_camera)
            align_movement = AlignMovement(charging_station_position_deamon, self._context.robot, align_move_distance=3,
                                           min_distance_to_target=15, marker_position_x=1170, time_sleep=1)
            align_movement.start(self.__align_done)
        except Exception as e:
            print(e)

    def __align_done(self):
        TOUCH_CHARGING_STATION_MOVE_DISTANCE = (50, 0)
        self._context.robot.move(TOUCH_CHARGING_STATION_MOVE_DISTANCE[0],
                                 TOUCH_CHARGING_STATION_MOVE_DISTANCE[1])
        time.sleep(2)
        self.recharge_done()

    def recharge_done(self):
        self._context.event_listener.notify_event(self._end_message)
