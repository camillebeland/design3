from maestro_control import maestro


class CameraRotationControl:
    def __init__(self, usb):
        # servomotors constants
        self.__MIDDLE = 6000
        self.__VERTICAL_MAX = 6000
        self.__VERTICAL_MIN = 2500
        self.__HORIZONTAL_MAX = 10000
        self.__HORIZONTAL_MIN = 2000
        self.__HORIZONTAL_CONVERSION_FACTOR = (self.__MIDDLE - self.__HORIZONTAL_MIN) / 90
        self.__VERTICAL_CONVERSION_FACTOR = (self.__VERTICAL_MAX - self.__VERTICAL_MIN) / 90
        # servomotors channels
        self.__HORIZONTAL = 4
        self.__VERTICAL = 5

        self.__controller = maestro.Controller(usb)
        self.set_vertical_speed()
        self.set_horizontal_speed()
        self.__controller.setRange(self.__HORIZONTAL, self.__HORIZONTAL_MIN, self.__HORIZONTAL_MAX)
        self.__controller.setRange(self.__VERTICAL, self.__VERTICAL_MIN, self.__VERTICAL_MAX)
        self.sleep()
    
    def sleep(self):
        self.__controller.setTarget(self.__HORIZONTAL, self.__MIDDLE)
        self.__controller.setTarget(self.__VERTICAL, self.__MIDDLE)

    # angle: in degrees, from -90 to 90
    def set_horizontal(self, angle):
        target = int(angle * self.__HORIZONTAL_CONVERSION_FACTOR) + self.__MIDDLE
        self.__controller.setTarget(self.__HORIZONTAL, target)

    # angle: in units, from 0 to 90
    def set_vertical(self, angle):
        target = int(angle * self.__VERTICAL_CONVERSION_FACTOR) + self.__VERTICAL_MIN
        self.__controller.setTarget(self.__VERTICAL, target)

    # 0 = max speed
    # 1 = min speed (1 minute for complete rotation)
    # 60 = 1 second pour complete rotation
    def set_horizontal_speed(self, speed=0):
        self.__controller.setSpeed(self.__HORIZONTAL, speed)

    # 0 = max speed
    # 1 = min speed (1 minute for complete rotation)
    # 60 = 1 second pour complete rotation
    def set_vertical_speed(self, speed=0):
        self.__controller.setSpeed(self.__VERTICAL, speed)