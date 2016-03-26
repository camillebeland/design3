from robot.arduino_validator import ArduinoValidator
from robot.errors.invalid_percentage_error import InvalidPercentageError

from time import sleep

def encode(string):
    return string.encode(encoding='utf8')


class Battery:

    def __init__(self, serial_port):
        self.serial_port = serial_port
        self.arduino_validator = ArduinoValidator()

    def get_level(self):
        self.serial_port.write(encode("(b)"))
        percentage_char = self.serial_port.read()

        try :
            percentage = ord(percentage_char)
            percentage_is_valid = self.arduino_validator.validate_percentage(percentage)
        except TypeError:
            percentage_is_valid = False 

        if percentage_is_valid :
            return percentage
        return -1
