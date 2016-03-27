from base_station.vision.image_wrapper import ImageWrapper

class VisionService:
    def __init__(self, camera, shape_detector, treasure_detector, table_calibrator, robot_detector):
        self.__camera = camera
        self.__shape_detector = shape_detector
        self.__treasure_detector = treasure_detector
        self.__table_calibrator = table_calibrator
        self.__robot_detector = robot_detector
        self.worldmap_contour = {}

    def build_map(self):
        image = ImageWrapper(self.__camera.get_frame())
        image = image.mask_image(self.worldmap_contour['table_contour'])
        circles, pentagons, squares, triangles, treasures = [], [], [], [], []

        triangles_red_upper, pentagons_red_upper, squares_red_upper, circles_red_upper = self.__find_polygon_color__(image, 'red_upper')
        triangles_red_lower, pentagons_red_lower, squares_red_lower, circles_red_lower = self.__find_polygon_color__(image, 'red_lower')
        triangles_green, pentagons_green, squares_green, circles_green = self.__find_polygon_color__(image, 'green')
        triangles_blue, pentagons_blue, squares_blue, circles_blue = self.__find_polygon_color__(image, 'blue')
        triangles_yellow, pentagons_yellow, squares_yellow, circles_yellow = self.__find_polygon_color__(image, 'yellow')

        triangles = triangles_green + triangles_blue + triangles_red_upper, triangles_red_lower + triangles_yellow
        circles = circles_green + circles_blue + circles_red_upper + circles_red_lower + circles_yellow
        pentagons = pentagons_green + pentagons_blue + pentagons_red_upper + pentagons_red_lower + pentagons_yellow
        squares = squares_green + squares_blue + squares_red_upper + squares_red_lower + squares_yellow

        treasures.extend(self.__treasure_detector.find_treasures(image, default_camille_polygon_params))

        worldmap = {
            'circles': circles,
            'triangles': triangles,
            'pentagons': pentagons,
            'squares': squares,
            'treasures': treasures
        }
        return worldmap

    def __find_polygon_color__(self, image, color):
        squares, pentagons, triangles, circles = self.__shape_detector.find_polygon_color(image, color, default_camille_polygon_params)
        if color is 'red_lower' or color is 'red_upper':
            color = 'red'
        for poly in circles:
            poly['shape'] = 'circle'
            poly['color'] = color
        for poly in squares:
            poly['shape'] = 'square'
            poly['color'] = color
        for poly in triangles:
            poly['shape'] = 'triangles'
            poly['color'] = color
        for poly in pentagons:
            poly['shape'] = 'pentagons'
            poly['color'] = color
        return triangles, pentagons, squares, circles

    def find_robot_position(self):
        image = ImageWrapper(self.__camera.get_frame())
        image = image.mask_image(self.worldmap_contour['table_contour'])
        purple_circle = self.__robot_detector.find_circle_color(image, default_camille_circle_params)
        purple_square = self.__robot_detector.find_polygon_color(image, find_robot_position_param)
        if not purple_circle or not purple_square:
            return {}
        else:
            angle = self.__find_angle_between__(purple_circle[0], purple_square[0])
            robot_position = {
                'center': ((purple_square[0]['x'] + purple_circle[0]['x'])/2, (purple_square[0]['y'] + purple_circle[0]['y'])/2),
                'angle': angle
            }
            return {'center' : robot_position['center'],
                    'angle': robot_position['angle']}

    def init_worldmap_contour(self):
        worldmap_contour = {}
        print('trying to get calibration data')
        while not worldmap_contour:
            image = ImageWrapper(self.__camera.get_frame())
            worldmap_contour = self.__table_calibrator.get_table_contour(image, default_camille_polygon_params)
        print('got calibration data')
        self.worldmap_contour = worldmap_contour

    def get_calibration_data(self):
        return self.worldmap_contour

    def __find_angle_between__(self, point1, point2):
        from math import atan2, degrees
        dx = point1['x'] - point2['x']
        dy = point1['y'] - point2['y']
        angle_in_rad = atan2(dy, dx)
        angle_in_deg = degrees(angle_in_rad)
        return -angle_in_deg


default_camille_circle_params = {
    'median_blur_kernel_size' : 5,
    'gaussian_blur_kernel_size' : 9,
    'gaussian_blur_sigma_x' : 2,
    'hough_circle_min_distance' : 10,
    'hough_circle_param1' : 50,
    'hough_circle_param2' : 30,
    'hough_circle_min_radius' : 20,
    'hough_circle_max_radius' : 120
}

default_camille_polygon_params = {
    'median_blur_kernel_size' : 5,
    'gaussian_blur_kernel_size' : 11,
    'gaussian_blur_sigma_x' : 0,
    'canny_threshold1' : 0,
    'canny_threshold2' : 50,
    'canny_aperture_size' : 5,
    'dilate_kernel_size' : 0,
    'dilate_iterations' : 2,
    'erode_kernel_size' : 0,
    'erode_iterations' : 2,
    'polygonal_approximation_error' : 4
}

find_robot_position_param = {
    'median_blur_kernel_size' : 5,
    'gaussian_blur_kernel_size' : 11,
    'gaussian_blur_sigma_x' : 0,
    'canny_threshold1' : 0,
    'canny_threshold2' : 50,
    'canny_aperture_size' : 5,
    'dilate_kernel_size' : 0,
    'dilate_iterations' : 2,
    'erode_kernel_size' : 0,
    'erode_iterations' : 2,
    'polygonal_approximation_error' : 4
}