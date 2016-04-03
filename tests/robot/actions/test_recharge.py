from robot.actions.recharge import RechargeAction
from robot.action import Action
from unittest.mock import *


class TestRecharge:
    def test_start_should_call_recharge_on_robot(self):
        # Given
        mock_robot = Mock()
        full_capacitor_value = 90
        mock_robot.get_capacitor_charge.return_value = full_capacitor_value
        recharge_action = RechargeAction(mock_robot, Mock(), Mock(), Mock())

        # When
        recharge_action.start()

        # Then
        mock_robot.start_recharge_magnet.assert_called_once_with()