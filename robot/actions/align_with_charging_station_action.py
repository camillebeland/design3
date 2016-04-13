from robot.action import Action
from robot.align_movement import AlignMovement
from robot.vision.charging_station_position_deamon import ChargingStationPositionDeamon
import time


class AlignWithChargingStationAction(Action):
    def start(self):
        self.running = True
        self._context.robot.set_camera_angle(10, 0)
        time.sleep(2)
        try:
            ratio = self._context.worldmap.get_pixel_per_meter_ratio()
            charging_station_position_deamon = ChargingStationPositionDeamon(self._context.embedded_camera)
            align_movement = AlignMovement(charging_station_position_deamon, self._context.robot, align_move_distance=0.001 * ratio,
                                           min_distance_to_target=2, marker_position_x=1270, time_sleep=0.20)
            align_movement.start(self.__align_done)
        except Exception as e:
            self.running = False
            print(e)

    def __align_done(self):
        TOUCH_CHARGING_STATION_MOVE_DISTANCE = (60, 0)
        self._context.robot.move(TOUCH_CHARGING_STATION_MOVE_DISTANCE[0],
                                 TOUCH_CHARGING_STATION_MOVE_DISTANCE[1])
        time.sleep(1)
        self._context.robot.stop()
        self._context.robot.set_camera_angle(90, 0)
        self.recharge_done()

    def recharge_done(self):
        if self.running:
            self._context.event_listener.notify_event(self._end_message)
        self.running = False

    def stop(self):
        print("Align with charging station asked to stop")
        self._context.robot.stop()
        self.running = False
