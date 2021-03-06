from vision_utils.image_wrapper import ImageWrapper
import cv2


class VisionService:
    def __init__(self, camera, shape_detector, treasure_detector, table_calibrator, robot_detector, charging_station_detector):
        self.__camera = camera
        self.__shape_detector = shape_detector
        self.__treasure_detector = treasure_detector
        self.__table_calibrator = table_calibrator
        self.__robot_detector = robot_detector
        self.__charging_station_detector = charging_station_detector
        self.worldmap_contour = {}

    def build_map(self):
        image = self.eliminate_first_frames()
        image = image.mask_image(self.worldmap_contour['table_contour'])
        circles, pentagons, squares, triangles, treasures = [], [], [], [], []

        triangles_red, pentagons_red, squares_red, circles_red = self.__find_polygon_color__(image, 'red')
        triangles_green, pentagons_green, squares_green, circles_green = self.__find_polygon_color__(image, 'green')
        triangles_blue, pentagons_blue, squares_blue, circles_blue = self.__find_polygon_color__(image, 'blue')
        triangles_yellow, pentagons_yellow, squares_yellow, circles_yellow = self.__find_polygon_color__(image, 'yellow')

        triangles = triangles_green + triangles_blue + triangles_red + triangles_yellow
        circles = circles_green + circles_blue + circles_red + circles_yellow
        pentagons = pentagons_green + pentagons_blue + pentagons_red + pentagons_yellow
        squares = squares_green + squares_blue + squares_red + squares_yellow

        treasures.extend(self.__treasure_detector.find_treasures(image, find_treasures_param))

        charging_station = self.charging_station

        treasures = self.__filter_treasure_by_wall_side(treasures, self.worldmap_contour['table_contour'])

        worldmap = {
            'circles': circles,
            'triangles': triangles,
            'pentagons': pentagons,
            'squares': squares,
            'treasures': treasures,
            'charging-station': charging_station
        }

        return worldmap

    def eliminate_first_frames(self):
        for bad_frames in range(1, 11):
            frame = self.__camera.get_frame()
            image = ImageWrapper(frame)
        cv2.imwrite('island_frame.jpg', frame)
        return image

    def __find_polygon_color__(self, image, color):
        squares, pentagons, triangles, circles = self.__shape_detector.find_polygon_color(image, color, default_camille_polygon_params)
        for poly in circles:
            poly['shape'] = 'circle'
            poly['color'] = color
        for poly in squares:
            poly['shape'] = 'square'
            poly['color'] = color
        for poly in triangles:
            poly['shape'] = 'triangle'
            poly['color'] = color
        for poly in pentagons:
            poly['shape'] = 'pentagon'
            poly['color'] = color
        return triangles, pentagons, squares, circles

    def find_robot_position(self):
        image = ImageWrapper(self.__camera.get_frame())
        image = image.mask_image(self.worldmap_contour['table_contour'])
        purple_circle, purple_square = self.__robot_detector.find_polygon_color(image, find_robot_position_param)
        if purple_circle is None or purple_square is None:
            return {}
        else:
            angle = self.__find_angle_between__(purple_circle, purple_square)
            robot_position = {
                'center': ((purple_square['x'] + purple_circle['x'])/2, (purple_square['y'] + purple_circle['y'])/2),
                'angle': angle
            }
            return {'center': robot_position['center'],
                    'angle': robot_position['angle']}

    def init_worldmap_contour_and_charging_station(self):
        worldmap_contour = {}
        print('trying to get calibration data')
        while not worldmap_contour:
            image = ImageWrapper(self.__camera.get_frame())
            worldmap_contour = self.__table_calibrator.get_table_contour(image, default_camille_polygon_params)
        print('got calibration data')
        self.worldmap_contour = worldmap_contour
        image_for_charging_station = ImageWrapper(self.__camera.get_frame())
        masked_image = image_for_charging_station.mask_image(self.worldmap_contour['table_contour'])
        self.charging_station = self.__charging_station_detector.find_polygon_color(masked_image, default_camille_polygon_params,
                                                                           self.worldmap_contour["pixels_per_meter"])

    def get_calibration_data(self):
        return self.worldmap_contour

    def __find_angle_between__(self, point1, point2):
        from math import atan2, degrees
        dx = point1['x'] - point2['x']
        dy = point1['y'] - point2['y']
        angle_in_rad = atan2(dy, dx)
        angle_in_deg = degrees(angle_in_rad)
        return -angle_in_deg

    def __filter_treasure_by_wall_side(self, treasures, table_corners):
        treasures_filtered = list()
        for treasure in treasures:
            side = None
            approximated_left_limit = table_corners[0][0]
            approximated_top_limit = table_corners[2][1]
            approximated_bottom_limit = table_corners[0][1]
            approximated_right_limit = table_corners[1][0]
            tolerance = 200
            tolerance_right = 350

            if (approximated_bottom_limit - tolerance) <= treasure["y"] < (approximated_bottom_limit + tolerance):
                side = "bottom"
            elif (approximated_bottom_limit - tolerance) <= treasure["x"] < (approximated_left_limit + tolerance):
                side = "left"
            elif (approximated_top_limit - tolerance) <= treasure["y"] < (approximated_top_limit + tolerance):
                side = "top"
            if (approximated_right_limit - tolerance_right) <= treasure["x"] < approximated_right_limit:
                side = None

            if side is not None:
                treasures_filtered.append(treasure)

        return treasures_filtered


default_camille_circle_params = {
    'median_blur_kernel_size': 5,
    'gaussian_blur_kernel_size': 9,
    'gaussian_blur_sigma_x': 2,
    'hough_circle_min_distance': 10,
    'hough_circle_param1': 50,
    'hough_circle_param2': 30,
    'hough_circle_min_radius': 20,
    'hough_circle_max_radius': 120
}

default_camille_polygon_params = {
    'median_blur_kernel_size': 5,
    'gaussian_blur_kernel_size': 11,
    'gaussian_blur_sigma_x': 0,
    'canny_threshold1': 0,
    'canny_threshold2': 50,
    'canny_aperture_size': 5,
    'dilate_kernel_size': 0,
    'dilate_iterations': 2,
    'erode_kernel_size': 0,
    'erode_iterations': 2,
    'polygonal_approximation_error': 4
}

find_robot_position_param = {
    'median_blur_kernel_size': 5,
    'gaussian_blur_kernel_size': 11,
    'gaussian_blur_sigma_x': 0,
    'canny_threshold1': 0,
    'canny_threshold2': 50,
    'canny_aperture_size': 5,
    'dilate_kernel_size': 0,
    'dilate_iterations': 2,
    'erode_kernel_size': 0,
    'erode_iterations': 2,
    'polygonal_approximation_error': 4
}

find_treasures_param = {
    'blur_kernel_size': 7,
    'dilate_kernel_size': 0,
    'dilate_iterations': 3,
    'erode_kernel_size': 0,
    'erode_iterations': 3,
    'polygonal_approximation_error': 4
}