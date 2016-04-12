from robot.action import Action
from time import sleep


class PickUpTreasureAction(Action):
    def start(self):
        self.running = True
        print('Picking Up Treasure')
        self._context.robot.activate_magnet()
        sleep(0.2)
        self._context.robot.move(-15, 0)
        sleep(2)
        self._context.robot.lift_prehenseur_up()
        sleep(3)
        self._context.robot.deactivate_magnet()

        if self.running:
            self._context.event_listener.notify_event(self._end_message)
        self.running = False

    def stop(self):
        print("Pick up treasure asked to stop")
        self.running = False

