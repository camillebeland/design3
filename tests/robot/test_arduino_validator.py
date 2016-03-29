from unittest.mock import *
from nose.tools import *
from nose.tools import assert_equals

from robot.arduino_validator import ArduinoValidator


class TestArduinoValidator:

    def __init__(self):
        self.arduino_validator = ArduinoValidator()

    def test_validate_percentage_should_return_true_if_is_valid(self):
        # Given
        a_valid_percentage = 99

        # When
        is_valid = self.arduino_validator.validate_percentage(a_valid_percentage)

        # Then
        assert_true(is_valid)

    def test_validate_percentage_should_return_false_if_not_only_numbers(self):
        # Given
        an_invalid_percentage = "99a"

        # When
        is_valid = self.arduino_validator.validate_percentage(an_invalid_percentage)

        # Then
        assert_false(is_valid)

    def test_validate_percentage_should_return_false_if_below_0(self):
        # Given
        an_invalid_percentage = -1

        # When
        is_valid = self.arduino_validator.validate_percentage(an_invalid_percentage)

        # Then
        assert_false(is_valid)

    def test_validate_percentage_should_return_false_if_above_100(self):
        # Given
        an_invalid_percentage = 101

        # When
        is_valid = self.arduino_validator.validate_percentage(an_invalid_percentage)

        # Then
        assert_false(is_valid)