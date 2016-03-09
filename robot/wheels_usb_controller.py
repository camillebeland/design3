class WheelsUsbController:
    def __init__(self, serialport, wheelsusbcommands):
        self.serialport = serialport
        self.wheelsusbcommands = wheelsusbcommands

    def move(self, x_pos, y_pos):
        self.serialport.write(self.wheelsusbcommands.move(int(x_pos),int( y_pos)))

    def rotate(self, angle):
        angle = int(angle)%360
        if(angle > 180):
            angle -= 360

        if(angle < 0):
            self.serialport.write(self.wheelsusbcommands.rotate_left(-angle))
        else:
            self.serialport.write(self.wheelsusbcommands.rotate_right(angle))
