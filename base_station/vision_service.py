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
        circles.extend(self.__find_polygon_color__(image, 'circle', 'green'))
        circles.extend(self.__find_polygon_color__(image, 'circle', 'blue'))
        circles.extend(self.__find_polygon_color__(image, 'circle', 'yellow'))
        circles.extend(self.__find_polygon_color__(image, 'circle', 'red'))
        pentagons.extend(self.__find_polygon_color__(image, 'pentagon', 'green'))
        pentagons.extend(self.__find_polygon_color__(image, 'pentagon', 'blue'))
        pentagons.extend(self.__find_polygon_color__(image, 'pentagon', 'yellow'))
        pentagons.extend(self.__find_polygon_color__(image, 'pentagon', 'red'))
        triangles.extend(self.__find_polygon_color__(image, 'triangle', 'green'))
        triangles.extend(self.__find_polygon_color__(image, 'triangle', 'blue'))
        triangles.extend(self.__find_polygon_color__(image, 'triangle', 'yellow'))
        triangles.extend(self.__find_polygon_color__(image, 'triangle', 'red'))
        squares.extend(self.__find_polygon_color__(image, 'square', 'green'))
        squares.extend(self.__find_polygon_color__(image, 'square', 'blue'))
        squares.extend(self.__find_polygon_color__(image, 'square', 'yellow'))
        squares.extend(self.__find_polygon_color__(image, 'square', 'red'))
        treasures.extend(self.__treasure_detector.find_treasures(image, default_camille_polygon_params))

        worldmap = {
            'circles': circles,
            'triangles': triangles,
            'pentagons': pentagons,
            'squares': squares,
            'treasures': treasures
        }
        return worldmap

    def __find_polygon_color__(self, image, shape, color):
        if shape == 'circle':
            shapes = self.__shape_detector.find_circle_color(image, color, default_camille_circle_params)
        else:
            shapes = self.__shape_detector.find_polygon_color(image, shape, color, default_camille_polygon_params)
        for poly in shapes:
            poly['shape'] = shape
            poly['color'] = color
        return shapes

    def find_robot_position(self):
        image = ImageWrapper(self.__camera.get_frame())
        image = image.mask_image(self.worldmap_contour['table_contour'])
        purple_circle = self.__robot_detector.find_circle_color(image, default_camille_circle_params)
        purple_square = self.__robot_detector.find_polygon_color(image, default_camille_polygon_params)
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
        image = ImageWrapper(self.__camera.get_frame())
        worldmap_contour = self.__table_calibrator.get_table_contour(image, default_camille_polygon_params)
        self.worldmap_contour = worldmap_contour

    def get_calibration_data(self):
        image = ImageWrapper(self.__camera.get_frame())
        worldmap_contour = self.__table_calibrator.get_table_contour(image, default_camille_polygon_params)
        return worldmap_contour

    def __find_angle_between__(self, point1, point2):
        from math import atan2, degrees
        dx = point1['x'] - point2['x']
        dy = point1['y'] - point2['y']
        angle_in_rad = atan2(dy, dx)
        angle_in_deg = degrees(angle_in_rad)
        return angle_in_deg


default_camille_circle_params = {
    'median_blur_kernel_size' : 5,
    'gaussian_blur_kernel_size' : 9,
    'gaussian_blur_sigma_x' : 2,
    'hough_circle_min_distance' : 10,
    'hough_circle_param1' : 50,
    'hough_circle_param2' : 30,
    'hough_circle_min_radius' : 0,
    'hough_circle_max_radius' : 0
}

default_camille_polygon_params = {
    'median_blur_kernel_size' : 5,
    'gaussian_blur_kernel_size' : 5,
    'gaussian_blur_sigma_x' : 0,
    'canny_threshold1' : 0,
    'canny_threshold2' : 50,
    'canny_aperture_size' : 5,
    'dilate_kernel_size' : 5,
    'dilate_iterations' : 2,
    'erode_kernel_size' : 5,
    'erode_iterations' : 2,
    'polygonal_approximation_error' : 4
}