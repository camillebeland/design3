from robot.action import Action
import time

class RechargeAction(Action):
    def start(self):
        print('Recharging')
        self._context.robot.recharge_magnet(self.recharge_done)

    def recharge_done(self):
        self._context.robot.move(-100, 0)
        time.sleep(1)
        self._context.robot.move(0,180)
        self._context.event_listener.notify_event(self._end_message)

    def stop(self):
        raise NotImplementedError
