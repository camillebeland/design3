from robot.arduino_validator import ArduinoValidator
from robot.errors.invalid_percentage_error import InvalidPercentageError


def encode(string):
    return string.encode(encoding='utf8')


class Battery:

    def __init__(self, serial_port):
        self.serial_port = serial_port
        self.arduino_validator = ArduinoValidator()

    def get_level(self):
        # self.serial_port.write(encode("(b)"))
        # percentage_char = self.serial_port.read()
        # percentage = ord(percentage_char)
        # percentage_is_valid = self.arduino_validator.validate_percentage(percentage)
        # if not percentage_is_valid:
        #    raise InvalidPercentageError("Arduino returned percentage is not valid: " + str(percentage))
        # return percentage
        return 41
