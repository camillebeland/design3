from robot.action import Action
from robot.align_movement import AlignMovement
from robot.vision.charging_station_position_deamon import ChargingStationPositionDeamon


class AlignWithChargingStationAction(Action):
    def start(self):
        charging_station_position_deamon = ChargingStationPositionDeamon(self._context.embedded_camera)
        align_movement = AlignMovement(charging_station_position_deamon, self._context.robot)
        try:
            align_movement.start(self.__align_done)
        except Exception as e:
            print(e)

    def __align_done(self):
        pass