from robot.exceptions.invalid_manchester_code_exception import InvalidManchesterCodeException


def encode(string):
    return string.encode(encoding='utf8')


class ManchesterAntennaUsbController:

    def __init__(self, serial_port):
        self.serial_port = serial_port

    def __validate_manchester_code(self, code):
        is_valid = True
        if len(code) != 1:
            is_valid = False
        elif not str(code).isalpha():
            is_valid = False

        if not is_valid:
            raise InvalidManchesterCodeException("invalid code is: " + str(code))

    def get_manchester_code(self):
        self.serial_port.write(encode("(c)"))
        code = self.serial_port.read().decode(encoding='utf8')

        self.__validate_manchester_code(code)
        return code


