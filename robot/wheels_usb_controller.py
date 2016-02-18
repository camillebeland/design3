class WheelsUsbController:
    def __init__(self, serialport, wheelsusbcommands):
        self.serialport = serialport
        self.wheelsusbcommands = wheelsusbcommands

    def move(self, x_pos, y_pos):
        print("je suis dans les roues, {0}, {1}".format(x_pos, y_pos))
        self.serialport.write(self.wheelsusbcommands.move(x_pos, y_pos))

    def rotate(self, angle):
        angle = angle%360
        if(angle > 180):
            angle -= 360

        if(angle < 0):
            self.serialport.write(self.wheelsusbcommands.rotate_left(-angle))
        else:
            self.serialport.write(self.wheelsusbcommands.rotate_right(angle))
