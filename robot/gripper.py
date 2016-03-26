from robot.arduino_validator import ArduinoValidator


def encode(string):
    return string.encode(encoding='utf8')


class Gripper:

    def __init__(self, serial_port):
        self.serial_port = serial_port
        self.arduino_validator = ArduinoValidator()

    def get_capacitor_charge(self):
        self.serial_port.write(encode("(v)"))
        percentage_char = self.serial_port.read()

        try:
            percentage = ord(percentage_char)
            percentage_is_valid = self.arduino_validator.validate_percentage(percentage)
        except TypeError:
            percentage_is_valid = False

        if percentage_is_valid:
            return percentage
        return -1

    def set_mock_validator(self, mock_validator):
        self.arduino_validator = mock_validator
