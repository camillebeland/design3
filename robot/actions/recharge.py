from robot.action import Action


class RechargeAction(Action):
    def start(self):
        print('Recharging')
        self._context.robot.recharge_magnet(self.recharge_done)

    def recharge_done(self):
        self._context.event_listener.notify_event(self._end_message)
