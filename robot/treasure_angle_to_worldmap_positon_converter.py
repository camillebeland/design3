import math


class TreasureAngleToWorldmapPositionConverter:
    def __init__(self, table_calibration_service, treasure_angles, robot):
        self.table_calibration_service = table_calibration_service
        self.treasure_angles = treasure_angles
        self.robot_angle = robot.get_angle()
        self.robot_position = robot.get_position()

    def get_treasures(self):
        treasures = self.__convert_to_map_position__()
        return treasures

    def __convert_to_map_position__(self):
        treasures_angles = self.treasure_angles
        table_corners = self.table_calibration_service.get_table_corners()

        bottom_slope = (table_corners[0][1] - table_corners[1][1]) / (table_corners[0][0] - table_corners[1][0])
        bottom_offset = table_corners[0][1] - (bottom_slope * table_corners[0][0])
        rear_line = table_corners[0][0]

        top_slope = (table_corners[2][1] - table_corners[3][1]) / (table_corners[3][0] - table_corners[2][0])
        top_offset = table_corners[3][1] - (top_slope * table_corners[3][0])
        
        camera_position = self.__compute_camera_position__()

        detected_treasures = []
        for angle in treasures_angles:
            treasure_slope = -math.tan(math.radians(self.robot_angle-(63.53/2)+angle))
            treasure_offset = camera_position[1] - (treasure_slope * camera_position[0])
            treasure_bottom_x = (bottom_offset - treasure_offset) / (treasure_slope - bottom_slope)
            treasure_bottom_y = (bottom_slope * treasure_bottom_x) + treasure_offset
            treasure_top_x = (top_offset - treasure_offset) / (treasure_slope - top_slope)
            treasure_top_y = (top_slope * treasure_top_x) + treasure_offset
            treasure_rear_x = rear_line
            treasure_rear_y = (treasure_slope * treasure_rear_x) + treasure_offset
            distance_bottom = math.sqrt((camera_position[0] - treasure_bottom_x)**2 + (camera_position[1] - treasure_bottom_y)**2)
            distance_top = math.sqrt((camera_position[0] - treasure_top_x)**2 + (camera_position[1] - treasure_top_y)**2)
            distance_rear = math.sqrt((camera_position[0] - treasure_rear_x)**2 + (camera_position[1] - treasure_rear_y)**2)

            min_list = []
            if treasure_bottom_x < camera_position[0]:
                min_list.append(distance_bottom)
            if treasure_top_x < camera_position[0]:
                min_list.append(distance_top)
            min_list.append(distance_rear)

            treasure_distance = min(min_list)
            if treasure_distance == distance_bottom:
                detected_treasures.append({'x': treasure_bottom_x, 'y' : treasure_bottom_y})
            elif treasure_distance == distance_rear:
                detected_treasures.append({'x': treasure_rear_x, 'y' : treasure_rear_y})
            elif treasure_distance == distance_top:
                detected_treasures.append({'x': treasure_top_x, 'y' : treasure_top_y})
        return detected_treasures

    def __compute_camera_position__(self):
        position = self.robot_position
        angle = self.robot_angle
        rayon_robot = self.table_calibration_service.get_pixel_per_meter_ratio() * 0.15

        position_camera = (position.x + math.cos(math.radians(angle)) * rayon_robot, position.y - math.sin(math.radians(angle)) * rayon_robot)
        return position_camera



