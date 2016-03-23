from nose.tools import *
from unittest.mock import *
from nose.tools import assert_equals
from robot.manchester_antenna_usb_controller import ManchesterAntennaUsbController
from robot.invalid_manchester_code_error import InvalidManchesterCodeError
from robot.invalid_percentage_error import InvalidPercentageError


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
        actual_code = usb_controller.get_manchester_code()

        # Then assert expected exception is raised

    def test_get_capacitor_charge_should_return_percentage_if_its_valid(self):
        # Given
        mock_serial_port = Mock()
        a_valid_percentage = 99
        mock_serial_port.read.return_value = chr(a_valid_percentage)
        usb_controller = ManchesterAntennaUsbController(mock_serial_port)

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
        usb_controller = ManchesterAntennaUsbController(mock_serial_port)

        # When
        actual_code = usb_controller.get_capacitor_charge()

        # Then assert expected exception is raised