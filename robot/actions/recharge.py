from robot.action import Action
import time

class RechargeAction(Action):
    def start(self):
        self.running = True
        print('Recharging')
        self._context.robot.recharge_magnet(self.recharge_done)

    def recharge_done(self):
        self._context.robot.move(-40, 180)
        time.sleep(1)
        if self.running:
            self._context.event_listener.notify_event(self._end_message)
        self.running = False

    def stop(self):
        print("Recharge asked to stop")
        self.running = False

