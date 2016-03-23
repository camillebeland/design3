from nose.tools import *
from unittest.mock import *
from nose.tools import assert_equals
from robot.gripper import Gripper
from robot.invalid_manchester_code_error import InvalidManchesterCodeError
from robot.invalid_percentage_error import InvalidPercentageError


class TestGripper:

    def test_get_capacitor_charge_should_return_percentage_if_its_valid(self):
        # Given
        mock_serial_port = Mock()
        a_valid_percentage = 99
        mock_serial_port.read.return_value = chr(a_valid_percentage)
        usb_controller = Gripper(mock_serial_port)

        # When
        actual_percentage = usb_controller.get_capacitor_charge()

        # Then
        assert_equals(a_valid_percentage, actual_percentage)

    @raises(InvalidPercentageError)
    def test_get_capacitor_charge_should_raise_error_if_percentage_not_valid(self):
        # Given
        mock_serial_port = Mock()
        an_invalid_percentage = 101
        mock_serial_port.read.return_value = chr(an_invalid_percentage)
        usb_controller = Gripper(mock_serial_port)

        # When
        actual_code = usb_controller.get_capacitor_charge()

        # Then assert expected exception is raised