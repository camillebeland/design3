class Magnet:
    def __init__(self, serial_port, prehenseur):
        self.__serial_port = serial_port
        self.__prehenseur = prehenseur

    def activate(self):
        self.__serial_port.write('(ao)'.encode())

    def deactivate(self):
        self.__serial_port.write('(af)'.encode())

    def lift_up(self):
        self.__prehenseur.lift()

    def lift_down(self):
        self.__prehenseur.grab()
