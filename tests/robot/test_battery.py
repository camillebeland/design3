from unittest.mock import *

from nose.tools import *
from nose.tools import assert_equals

from robot.battery import Battery
from robot.errors.invalid_percentage_error import InvalidPercentageError


#class TestBattery:
#
#      def test_get_level_should_return_percentage_if_its_valid(self):
#     # Given
#     mock_serial_port = Mock()
#     a_percentage = 99
#     mock_serial_port.read.return_value = chr(a_percentage)
#     usb_controller = Battery(mock_serial_port)
#     mock_validator = Mock()
#     mock_validator.validate_percentage.return_value = True
#     usb_controller.set_mock_validator = mock_validator
#
#     # When
#     actual_percentage = usb_controller.get_level()
#
#     # Then
#     assert_equals(a_percentage, actual_percentage)
#
# @raises(InvalidPercentageError)
# def test_get_level_should_raise_error_if_percentage_not_valid(self):
#     # Given
#     mock_serial_port = Mock()
#     an_invalid_percentage = 101
#     mock_serial_port.read.return_value = chr(an_invalid_percentage)
#     usb_controller = Battery(mock_serial_port)
#     mock_validator = Mock()
#     mock_validator.validate_percentage.return_value = True
#     usb_controller.set_mock_validator = mock_validator
#
#     # When
#     actual_code = usb_controller.get_level()
#
#     # Then assert expected exception is raised
#TODO
