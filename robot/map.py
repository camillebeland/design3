
class Map:
    def __init__(self, width, height, robot_service, vision_daemon):
        self._width = width
        self._height = height
        self.__robot_service = robot_service
        self._robot_position = self.__robot_service.get_robot_position()
        self._robot_angle = 0
        self.vision_daemon = vision_daemon

    def set_robot_position(self):
        self._robot_position = self.__robot_service.get_robot_position()

    def set_robot_angle(self, angle):
        self._robot_angle = angle

    def get_robot_position(self):
        return self.vision_daemon.get_robot_position_from_vision()

    def get_robot_angle(self):
        return self._robot_angle

    def move_robot(self, delta_x, delta_y):
        delta = rotate_vector(- self._robot_angle, np.array([delta_x, delta_y]))
        self.set_robot_position(self._robot_position[0] + delta[0], self._robot_position[1] + delta[1])

    def rotate_robot(self, angle):
        self._robot_angle += angle
        self._robot_angle = self._robot_angle % 360

    def __is_inside_boundaries(self,x, y):
        return x > 0 and x < self._width and y > 0 and y < self._height

    def relative_position(self, position):
        return rotate_vector(self._robot_angle, np.array(position) - np.array(self._robot_position))