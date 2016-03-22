from robot.action import Action


class RechargeAction(Action):
    def start(self):
        alignment_correction = self.__embedded_camera.get_recharge_station_position()
        self.__robot.fine_move_to(alignment_correction)

