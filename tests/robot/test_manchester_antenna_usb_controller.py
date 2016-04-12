from unittest.mock import *

from nose.tools import *
from nose.tools import assert_equals

from robot.errors.invalid_manchester_code_error import InvalidManchesterCodeError
from robot.manchester_antenna_usb_controller import ManchesterAntennaUsbController


class TestManchesterAntennaUsbController:

    def test_get_manchester_code_should_return_code_if_is_valid(self):
        # Given
        mock_serial_port = Mock()
        a_valid_code = "A"
        mock_serial_port.read.return_value = a_valid_code.encode(encoding='utf8')
        usb_controller = ManchesterAntennaUsbController(mock_serial_port)

        # When
        actual_code = usb_controller.get_manchester_code()

        # Then
        assert_equals(a_valid_code, actual_code)

    @raises(InvalidManchesterCodeError)
    def test_get_manchester_code_should_raise_error_if_code_not_valid(self):
        # Given
        mock_serial_port = Mock()
        an_invalid_code = ""
        mock_serial_port.read.return_value = an_invalid_code.encode(encoding='utf8')
        usb_controller = ManchesterAntennaUsbController(mock_serial_port)

        # When
        usb_controller.get_manchester_code()

        # Then assert expected exception is raised