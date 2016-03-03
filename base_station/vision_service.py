from base_station.vision import Image
import cv2
class VisionService:
    def __init__(self, camera, shape_detector):
        self.__camera = camera
        self.__shape_detector = shape_detector

    def build_map(self):
        image = Image(self.__camera.get_frame())
        circles = self.__shape_detector.find_circle_color(image, 'red', default_camille_circle_params)
        triangles = self.__shape_detector.find_polygon_color(image, 'triangle', 'red', default_camille_polygon_params)
        pentagons = self.__shape_detector.find_polygon_color(image, 'pentagon', 'red', default_camille_polygon_params)
        squares = self.__shape_detector.find_polygon_color(image, 'square', 'red', default_camille_polygon_params)
        for circle in circles:
            circle['shape'] = 'circle'
            circle['color'] = 'red'
        for triangle in triangles:
            triangle['shape'] = 'triangle'
            triangle['color'] = 'red'
        for square in squares:
            square['shape'] = 'square'
            square['color'] = 'red'
        for pentagon in pentagons:
            pentagon['shape'] = 'pentagon'
            pentagon['color'] = 'red'
        worldmap = {
            'circles': circles,
            'triangles': triangles,
            'pentagons' : pentagons,
            'squares' : squares
        }
        return worldmap

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