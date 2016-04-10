from robot.action import Action
from time import sleep


class PickUpTreasureAction(Action):
    def start(self):
        print('Picking Up Treasure')
        self._context.robot.lift_prehenseur_down()
        sleep(1)
        self._context.robot.activate_magnet()
        sleep(0.2)
        self._context.robot.move(-15, 0)
        sleep(2)
        self._context.robot.lift_prehenseur_up()
        sleep(1)
        self._context.robot.deactivate_magnet()
        self._context.event_listener.notify_event(self._end_message)

    def stop(self):
        raise NotADirectoryError
