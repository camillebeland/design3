class WheelsUsbController:
    def __init__(self, serialport, wheels_usb_commands):
        self.serialport = serialport
        self.wheels_usb_commands = wheels_usb_commands

    def move(self, x_pos, y_pos):
        self.serialport.write(self.wheels_usb_commands.move(int(x_pos), int(y_pos)))

    def rotate(self, angle):
        angle = int(angle)%360
        if angle > 180:
            angle -= 360

        if angle < 0:
            self.serialport.write(self.wheels_usb_commands.rotate_left(-angle))
        else:
            self.serialport.write(self.wheels_usb_commands.rotate_right(angle))

    def stop(self):
        self.serialport.write(self.wheels_usb_commands.stop())
