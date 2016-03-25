from robot.invalid_manchester_code_error import InvalidManchesterCodeError
from robot.invalid_percentage_error import InvalidPercentageError


def encode(string):
    return string.encode(encoding='utf8')


class ManchesterAntennaUsbController:

    def __init__(self, serial_port):
        self.serial_port = serial_port

    def __validate_manchester_code(self, code):
        is_valid = True;
        if len(code) != 1:
            is_valid = False
        elif not str(code).isalpha():
            is_valid = False

        if not is_valid:
            raise InvalidManchesterCodeError("invalid code is: "+ str(code))

    def __validate_percentage(self, percentage):
        is_valid = True;

        if not str(percentage).isnumeric():
            is_valid = False
        elif int(percentage) < 0 or int(percentage) > 100:
            is_valid = False

        if not is_valid:
            raise InvalidPercentageError("Arduino returned percentage is not valid: "+ str(percentage))

    def get_manchester_code(self):
        self.serial_port.write(encode("(c)"))
        code = self.serial_port.read().decode(encoding='utf8')

        self.__validate_manchester_code(code)
        return code

    def get_battery_level(self):
        self.serial_port.write(encode("(b)"))
        percentage_char = self.serial_port.read()
        percentage = ord(percentage_char)
        self.__validate_percentage(percentage)
        return percentage

    def get_capacitor_charge(self):
        self.serial_port.write(encode("(v)"))
        percentage_char = self.serial_port.read()
        percentage = ord(percentage_char)
        self.__validate_percentage(percentage)
        return percentage

