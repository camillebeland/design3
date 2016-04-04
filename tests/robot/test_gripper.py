from unittest.mock import *
from nose.tools import assert_equals
from robot.gripper import Gripper


class TestGripper:

    def test_get_capacitor_charge_should_return_percentage_if_its_valid(self):
        # Given
        mock_serial_port = Mock()
        percentage_sent = 99
        mock_serial_port.read.return_value = chr(percentage_sent)
        usb_controller = Gripper(mock_serial_port)
        mock_validator = Mock()
        mock_validator.validate_percentage.return_value = True
        usb_controller.set_mock_validator = mock_validator

        # When
        actual_percentage = usb_controller.get_capacitor_charge()

        # Then
        assert_equals(percentage_sent, actual_percentage)

    def test_get_capacitor_charge_should_return_minus_one_if_percentage_not_valid(self):
        # Given
        mock_serial_port = Mock()
        an_invalid_percentage = 101
        mock_serial_port.read.return_value = chr(an_invalid_percentage)
        usb_controller = Gripper(mock_serial_port)
        mock_validator = Mock()
        mock_validator.validate_percentage.return_value = False
        usb_controller.set_mock_validator = mock_validator

        # When
        actual_code = usb_controller.get_capacitor_charge()

        # Then
        assert_equals(-1, actual_code)

