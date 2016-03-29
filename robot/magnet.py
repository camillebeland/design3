class Magnet:
    def __init__(self, serial_port):
        self.__serial_port = serial_port

    def activate(self):
        self.__serial_port.write('(ao)'.encode())

    def deactivate(self):
        self.__serial_port.write('(af)'.encode())
