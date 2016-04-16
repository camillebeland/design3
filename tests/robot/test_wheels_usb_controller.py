# from nose.tools import *
# from robot.wheels_usb_controller import WheelsUsbController
#
# FORWARD = 100
# BACKWARD = -100
# LEFT = 50
# RIGHT = -50
# POSITIVE_ANGLE = 42
# NEGATIVE_ANGLE = -42
# LARGE_ANGLE = 190
# SMALL_ANGLE = 170
# ANGLE_LARGER_THAN_CIRCLE = 760
# ANGLE_MODULO_CIRCLE = 40
# LARGE_NEGATIVE_ANGLE = -190
#
# FORWARDCOMMAND = "gogogo"
# BACKWARDCOMMAND = "RETREAT"
# LEFTCOMMAND = "FLANK LEFT"
# RIGHTCOMMAND = "TOOOLDFORTHIS"
# ROTATERIGHTCOMMAND = "Blerp"
# ROTATELEFTCOMMAND = "antilope"
#
#
# class MockSerial:
#     def __init__(self):
#         self.command = ""
#
#     def write(self, command):
#         self.command = command
#
#
# class MockUsbCommands:
#     def __init__(self):
#         pass
#
#     def move(self, x, y):
#         if x == FORWARD and y == 0:
#             return FORWARDCOMMAND
#         if x == BACKWARD and y == 0:
#             return BACKWARDCOMMAND
#         if x == 0 and y == LEFT:
#             return LEFTCOMMAND
#         if x == 0 and y == RIGHT:
#             return RIGHTCOMMAND
#
#     def rotate_right(self, angle):
#         return ROTATERIGHTCOMMAND+angle.__str__()
#
#     def rotate_left(self, angle):
#         return ROTATELEFTCOMMAND+angle.__str__()
#
# serialport = MockSerial()
# usbcommands = MockUsbCommands()
#
# wheels = WheelsUsbController(serialport, usbcommands)
#
#
# def test_move_wheel_forward_then_write_the_command_forward_in_serial_port():
#     wheels.move(FORWARD,0)
#     assert_equal(FORWARDCOMMAND, serialport.command)
#
#
# def test_move_wheel_backward_then_write_the_command_backward_in_serial_port():
#     wheels.move(BACKWARD,0)
#     assert_equal(BACKWARDCOMMAND, serialport.command)
#
#
# def test_move_wheel_left_then_write_the_command_left_in_serial_port():
#     wheels.move(0,LEFT)
#     assert_equal(LEFTCOMMAND, serialport.command)
#
#
# def test_move_wheel_right_then_write_the_command_right_in_serial_port():
#     wheels.move(0,RIGHT)
#     assert_equal(RIGHTCOMMAND, serialport.command)
#
#
# def test_rotate_wheel_for_positive_angle_then_command_rotate_right_in_serial_port():
#     wheels.rotate(POSITIVE_ANGLE)
#     assert_equal(ROTATERIGHTCOMMAND+POSITIVE_ANGLE.__str__(), serialport.command)
#
#
# def test_rotate_wheel_for_negative_angle_then_command_rotate_left_in_serial_port():
#     wheels.rotate(NEGATIVE_ANGLE)
#     assert_equal(ROTATELEFTCOMMAND+POSITIVE_ANGLE.__str__(), serialport.command)
#
#
# def test_rotate_wheel_for_large_angle_then_command_rotate_left_small_angle_in_serial_port():
#     wheels.rotate(LARGE_ANGLE)
#     assert_equal(ROTATELEFTCOMMAND+SMALL_ANGLE.__str__(), serialport.command)
#
#
# def test_rotate_wheel_for_angle_larger_than_circle_then_rotate_modulo_2pi_in_serial_port():
#     wheels.rotate(ANGLE_LARGER_THAN_CIRCLE)
#     assert_equal(ROTATERIGHTCOMMAND+ANGLE_MODULO_CIRCLE.__str__(), serialport.command)
#
#
# def test_rotate_wheel_for_large_negative_angle_then_command_rotate_right_small_angle_in_serial_port():
#     wheels.rotate(LARGE_NEGATIVE_ANGLE)
#     assert_equal(ROTATERIGHTCOMMAND+SMALL_ANGLE.__str__(), serialport.command)
