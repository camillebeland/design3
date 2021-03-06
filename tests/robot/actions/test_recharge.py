from robot.actions.recharge import RechargeAction
from robot.action import Action
from unittest.mock import *
from nose.tools import *


class TestRecharge:
    def test_start_should_call_recharge_on_robot(self):
        # Given
        mock_robot = Mock()
        mock_context = Mock()
        mock_context.robot = mock_robot
        recharge_action = RechargeAction(mock_context, Mock())

        # When
        recharge_action.start()

        # Then
        assert_true(mock_robot.recharge_magnet.called)
