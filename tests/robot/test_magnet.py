from nose.tools import *
from unittest.mock import *

from robot.robot import Robot

class TestMagnet:

    def test_activate_magnet(self):
        # Given
        magnet = Mock()
        robot = Robot(Mock(), Mock(), Mock(), Mock(), Mock(), magnet)

        # When
        robot.activate_magnet()

        #Then
        magnet.activate.assert_called_once_with()

    def test_deactivate_magnet(self):
        # Given
        magnet = Mock()
        robot = Robot(Mock(), Mock(), Mock(), Mock(), Mock(), magnet)

        # When
        robot.deactivate_magnet()

        # Then
        magnet.deactivate.assert_called_once_with()

    def test_when_activate_magnet_then_log_activation(self):
        # Given
        robot_service = Mock()
        robot = Robot(Mock(), Mock(), Mock(), robot_service, Mock(), Mock())

        # When
        robot.activate_magnet()

        # Then
        robot_service.log_info.assert_called_once_with("Magnet Activation")

    def test_when_deactivate_magnet_then_log_activation(self):
        # Given
        robot_service = Mock()
        robot = Robot(Mock(), Mock(), Mock(), robot_service, Mock(), Mock())

        # When
        robot.deactivate_magnet()

        # Then
        robot_service.log_info.assert_called_once_with("Magnet Deactivation")
