
class WheelsCorrectionLayer:
    def __init__(self, wheels, ratio):
        self.__wheels = wheels
        self.__ratio = ratio

    def move(self, x_pos, y_pos):
        self.__wheels.move(x_pos / self.__ratio * 1000, y_pos / self.__ratio * 1000)

    def rotate(self, angle):
        self.__wheels.rotate(angle)

    def stop(self):
        self.__wheels.stop()
