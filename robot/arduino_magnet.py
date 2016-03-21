
class ArduinoMagnet:
    def __init__(self, serialport, usbcommands):
        self.__serialport = serialport
        self.__usbcommands = usbcommands

    def activate(self):
        self.__serialport.write(self.__usbcommands.activate_magnet())

    def deactivate(self):
        self.__serialport.write(self.__usbcommands.deactivate_magnet())
