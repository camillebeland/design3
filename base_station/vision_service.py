from base_station.image_wrapper import ImageWrapper


class VisionService:
    def __init__(self, camera, shape_detector):
        self.__camera = camera
        self.__shape_detector = shape_detector

    def build_map(self):
        image = ImageWrapper(self.__camera.get_frame())
        circles, pentagons, squares, triangles = [], [], [], []
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

        worldmap = {
            'circles': circles,
            'triangles': triangles,
            'pentagons': pentagons,
            'squares': squares
        }
        return worldmap

    def __find_polygon_color__(self, image, shape, color):
        if shape == 'circle':
            shapes = self.__shape_detector.find_circle_color(image, color, default_camille_circle_params)
        else:
            shapes = self.__shape_detector.find_polygon_color_remi(image, shape, color, default_remi_polygon_params)
        for poly in shapes:
            poly['shape'] = shape
            poly['color'] = color
        return shapes

default_camille_circle_params = {
    'median_blur_kernel_size' : 5,
    'gaussian_blur_kernel_size' : 9,
    'gaussian_blur_sigma_x' : 2,
    'hough_circle_min_distance' : 50,
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
    'dilate_kernel_size' : 51,
    'dilate_ierations' : 1,
    'erode_kernel_size' : 51,
    'erode_iterations' : 1,
    'polygonal_approximation_error' : 4
}

default_remi_polygon_params = {
    'gaussian_blur_kernel_size' : 15,
    'gaussian_blur_sigma_x' : 0,
    'dilate_kernel_size' : 5,
    'dilate_ierations' : 1,
    'erode_kernel_size' : 5,
    'erode_iterations' : 1,
    'shape_min_height': 40,
    'shape_max_height': 40,
    'shape_min_width': 140,
    'shape_max_width': 140,
    'polygonal_approximation_error' : 0.015
}