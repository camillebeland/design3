from robot.invalid_manchester_code_error import InvalidManchesterCodeError
from robot.invalid_percentage_error import InvalidPercentageError


def encode(string):
    return string.encode(encoding='utf8')


class Gripper:

    def __init__(self, serial_port):
        self.serial_port = serial_port

    def __validate_percentage(self, percentage):
        is_valid = True;

        if not str(percentage).isnumeric():
            is_valid = False
        elif int(percentage) < 0 or int(percentage) > 100:
            is_valid = False

        if not is_valid:
            raise InvalidPercentageError("Arduino returned percentage is not valid: "+ str(percentage))

    def get_capacitor_charge(self):
        self.serial_port.write(encode("(v)"))
        percentage_char = self.serial_port.read()
        percentage = ord(percentage_char)
        print(percentage)
        self.__validate_percentage(percentage)
        return percentage

