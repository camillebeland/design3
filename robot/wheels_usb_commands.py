
def encode(string):
    return string.encode(encoding='utf8')

class WheelsUsbCommands:
    def __init__(self):
        pass

    def stop(self):
        return encode("(s)")

    def rotate_left(self, angle):
        return self.__rotate('l', angle)

    def rotate_right(self, angle):
        return self.__rotate('r', angle)

    def __rotate(self, direction, angle):
        assert(abs(angle)<180)
        return encode("(r"+direction)+bytes([angle])+encode(")")


    def move_slow(self, x_pos, y_pos):
        return self.__move('m', x_pos, y_pos)

    def move(self, x_pos, y_pos):
        return self.__move('M', x_pos, y_pos)

    def __move(self, speed, x_pos, y_pos):
        x_pos = self.__apply_limits(x_pos)
        y_pos = self.__apply_limits(y_pos)
        return encode("("+speed)+bytes([x_pos//256])+bytes([x_pos % 256]) + bytes([y_pos//256])+ bytes([y_pos%256])+encode(")")

    def __apply_limits(self, number):
        number = min(number, 32767)
        number = max(number, -32768)
        if(number < 0):
            number = -number + 32768
        return number
