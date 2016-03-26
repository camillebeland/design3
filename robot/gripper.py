from robot.errors.invalid_percentage_error import InvalidPercentageError
from robot.arduino_validator import ArduinoValidator


def encode(string):
    return string.encode(encoding='utf8')


class Gripper:

    def __init__(self, serial_port):
        self.serial_port = serial_port
        self.arduino_validator = ArduinoValidator()

    def get_capacitor_charge(self):
        # self.serial_port.write(encode("(v)"))
        # percentage_char = self.serial_port.read()
        # percentage = ord(percentage_char)
        # percentage_is_valid = self.arduino_validator.validate_percentage(percentage)
        # if not percentage_is_valid:
        #    raise InvalidPercentageError("Arduino returned percentage is not valid: " + str(percentage))
        #
        # return percentage
        return 41

    def set_mock_validator(self, mock_validator):
        self.arduino_validator = mock_validator
