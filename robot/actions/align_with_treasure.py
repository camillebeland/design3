from robot.action import Action
from robot.align_movement import AlignMovement
from robot.vision.treasure_position_deamon import TreasurePositionDeamon


class AlignWithTreasureAction(Action):
    def start(self):
        treasure_position_deamon = TreasurePositionDeamon(self._context.embedded_camera)
        align_movement = AlignMovement(treasure_position_deamon, self._context.robot)
        align_movement.start(self.__align_done)

    def __align_done(self):
        self._context.event_listener.notify_event(self._end_message)
