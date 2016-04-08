from robot.action import Action
from time import sleep


class DropDownTreasure(Action):
    def start(self):
        print('Dropping Treasure')
        self._context.robot.activate_magnet()
        self._context.robot.lift_prehenseur_down()
        sleep(1)
        self._context.robot.deactivate_magnet()
        self._context.event_listener.notify_event(self._end_message)

    def stop(self):
        raise NotImplementedError
