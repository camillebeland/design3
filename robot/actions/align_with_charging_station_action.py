from robot.action import Action
from robot.align_movement import AlignMovement
from robot.vision.charging_station_position_deamon import ChargingStationPositionDeamon


class AlignWithChargingStationAction(Action):
    def start(self):
        charging_station_position_deamon = ChargingStationPositionDeamon(self._context.embedded_camera)
        align_movement = AlignMovement(charging_station_position_deamon, self._context.robot)
        align_movement.start(self.__align_done)

    def __align_done(self):
        self._context.event_listener.notify_event(self._end_message)
