from robot.robot import Robot
from unittest.mock import *
import unittest


class TestRobot:
    def setup(self):
        self.mock_wheels = Mock()
        self.mock_map = Mock()
        self.robot = Robot(self.mock_wheels, self.mock_map)

    def test_rotate_should_call_rotate_on_wheels(self):
        # Given a test robot
        some_angle = 30

        # When
        self.robot.rotate(some_angle)

        # Then
        self.mock_wheels.rotate.assert_called_once_with(some_angle)
