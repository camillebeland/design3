from time import sleep
from threading import Thread
from robot.arduino_validator import ArduinoValidator


class Magnet:
    def __init__(self, serial_port, prehenseur):
        self.__serial_port = serial_port
        self.__prehenseur = prehenseur
        self.arduino_validator = ArduinoValidator()

    def activate(self):
        self.__serial_port.write('(ao)'.encode())

    def deactivate(self):
        self.__serial_port.write('(af)'.encode())

    def lift_up(self):
        self.__prehenseur.lift()

    def lift_down(self):
        self.__prehenseur.grab()

    def recharge(self, callback):
        self.thread = Thread(target=self.__thread_recharge, args=(callback,))
        self.thread.setDaemon(True)
        self.thread.start()

    def __thread_recharge(self, callback):
        self.__start_recharge()
        while self.get_charge() < 90.0:
            print(self.get_charge())
            sleep(1)
        self.__stop_recharge()
        callback()

    def __start_recharge(self):
        self.__serial_port.write('(ac)'.encode())

    def __stop_recharge(self):
        self.__serial_port.write('(ad)'.encode())

    def discharge(self):
        self.__start_discharge()
        while self.get_charge() > 5.0:
            print(self.get_charge())
            sleep(1)
        self.__stop_discharge()

    def __start_discharge(self):
        self.__serial_port.write('(ax)'.encode())

    def __stop_discharge(self):
        self.__serial_port.write('(az)'.encode())

    def get_charge(self):
        self.__serial_port.write('(v)'.encode())
        percentage_char = self.__serial_port.read()
        try:
            percentage = ord(percentage_char)
            percentage_is_valid = self.arduino_validator.validate_percentage(percentage)
        except TypeError:
            percentage_is_valid = False

        if percentage_is_valid:
            return percentage
        else:
            return -1

    def set_mock_validator(self, mock_validator):
        self.arduino_validator = mock_validator

