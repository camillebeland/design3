class Magnet:
    def __init__(self, serial_port):
        self.__serial_port = serial_port

    def activate(self):
        self.__serial_port.write('(ao)'.encode())

    def deactivate(self):
        self.__serial_port.write('(af)'.encode())

    def start_recharge(self):
        self.__serial_port.write('(ac)'.encode())

    def stop_recharge(self):
        self.__serial_port.write('(ad)'.encode())

    def start_discharge(self):
        self.__serial_port.write('(ax)'.encode())

    def stop_discharge(self):
        self.__serial_port.write('(az)'.encode())
