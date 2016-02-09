def stop():
    return "(s)"

def rotate_left(angle):
    return "(rl{0})".format(chr(angle))

def rotate_right(angle):
    return "(rr{0})".format(chr(angle))

def move_slow(x_pos, y_pos):
    return "(m{0}{1}{2}{3})".format(chr(x_pos//256), chr(x_pos % 256), chr(y_pos//256), chr(y_pos%256))

def move(x_pos, y_pos):
    return "(M{0}{1}{2}{3})".format(chr(x_pos//256), chr(x_pos % 256), chr(y_pos//256), chr(y_pos%256))
