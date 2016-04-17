from maestro_control import maestro
import time


class PrehenseurRotationControl:

    def __init__(self, usb):
        # servomotors constants
        self.__MIN = 4300
        self.__MAX = 8800
        self.__CHANNEL = 3
        self.__CONV_FACTOR = (self.__MAX - self.__MIN)/90
        self.__controller = maestro.Controller(usb)
        self.__controller.setRange(self.__CHANNEL, self.__MIN, self.__MAX)
        cmd = chr(0xa1)
        usb.write(cmd.encode(encoding='UTF-8'))

    # 0 = max speed
    # 1 = min speed (1 minute for complete rotation)
    # 60 = 1 second pour complete rotation
    def setSpeed(self, speed=40):
        self.__controller.setSpeed(self.__CHANNEL, speed)

    def grab(self):
        self.__controller.setTarget(self.__CHANNEL, self.__MIN)

    def lift(self):
        self.setSpeed()
        time.sleep(0.5)
        self.__controller.setTarget(self.__CHANNEL, self.__MAX)
