def encode(string):
    return string.encode(encoding='utf8')


class ManchesterAntennaUsbController:

    def __init(self, serial_port):
        self.serial_port = serial_port

    def get_manchester_code(self):
        self.serial_port.write(encode("(c)"))
        code = self.serial_port.read()
        return code

