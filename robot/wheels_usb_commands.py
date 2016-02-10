def stop():
    return "(s)"

def rotate_left(angle):
    return __rotate('l', angle)

def rotate_right(angle):
    return __rotate('r', angle)

def __rotate(direction, angle):
    assert(abs(angle)<180)
    return "(r"+direction+"{0})".format(chr(angle))


def move_slow(x_pos, y_pos):
    return __move('m', x_pos, y_pos)

def move(x_pos, y_pos):
    return __move('M', x_pos, y_pos)

def __move(speed, x_pos, y_pos):
    x_pos = __apply_limits(x_pos)
    y_pos = __apply_limits(y_pos)
    return "("+speed+"{0}{1}{2}{3})".format(chr(x_pos//256), chr(x_pos % 256), chr(y_pos//256), chr(y_pos%256))

def __apply_limits(number):
    number = min(number, 32767)
    number = max(number, -32768)
    if(number < 0):
        number = -number + 32768
    return number

