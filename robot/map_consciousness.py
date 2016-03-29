
class MapConsciousness:
    def __init__(self, actual_map, initial_position, initial_angle):
        self.__robot_position = initial_position
        self.__robot_angle = initial_angle
        self.__map = actual_map
        self.__distance_threshold = 50

    def get_robot_position(self):
        new_position = self.__map.get_robot_position()
        if new_position.distance(self.__robot_position) < self.__distance_threshold:
            self.__robot_position = new_position
        return self.__robot_position

    def get_robot_angle(self):
        return self.__map.get_robot_angle()
