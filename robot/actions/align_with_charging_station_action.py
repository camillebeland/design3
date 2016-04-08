from robot.action import Action
from robot.align_movement import AlignMovement
from robot.vision.charging_station_position_deamon import ChargingStationPositionDeamon
import time
class AlignWithChargingStationAction(Action):
    def start(self):
        charging_station_position_deamon = ChargingStationPositionDeamon(self._context.embedded_camera)
        align_movement = AlignMovement(charging_station_position_deamon, self._context.robot)
        self._context.robot.set_camera_angle(25, 0)
        time.sleep(2)
        try:
            align_movement.start(self.__align_done)
        except Exception as e:
            print(e)

    def __align_done(self):
        self._context.robot.move(30, 0)