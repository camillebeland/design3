from robot.action import Action


class RechargeAction(Action):
    def start(self):
        self._robot.recharge_magnet(self.recharge_done)

    def recharge_done(self):
        print('recharge done')
