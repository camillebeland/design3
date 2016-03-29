import cv2
import base_station.vision.vision_utils as utils

class RobotDetector:
    def find_polygon_color(self, image, parameters, opencv=cv2):
        erode_kernel_size = parameters['erode_kernel_size']
        erode_iterations = parameters['erode_iterations']
        dilate_kernel_size = parameters['dilate_kernel_size']
        dilate_iterations = parameters['dilate_iterations']
        gaussian_blur_kernel_size = parameters['gaussian_blur_kernel_size']
        gaussian_blur_sigma_x = parameters['gaussian_blur_sigma_x']


        def approx_polygon(contour):
            epsilon = 0.04*cv2.arcLength(contour, True)
            return opencv.approxPolyDP(contour, epsilon, True)

        contours = (image
                    .filter_gaussian_blur((gaussian_blur_kernel_size,gaussian_blur_kernel_size),gaussian_blur_sigma_x)
                    .filter_by_color(hsv_range['purple'])
                    .erode(erode_kernel_size, erode_iterations)
                    .dilate(dilate_kernel_size, dilate_iterations)
                    .find_contours())

        robot_square = None
        robot_circle = None
        for contour in contours:
            leftest_vertex, lowest_vertex, rightest_vertex, upper_vertex = utils.find_shape_height_and_lenght(contour)
            detected_shape_length = abs(rightest_vertex - leftest_vertex)
            detected_shape_height = abs(upper_vertex - lowest_vertex)
            approx = approx_polygon(contour)

            if self.__is_a_robot_position_marker__(detected_shape_length, detected_shape_height) and len(approx) == edges['square']:
                marker = utils.find_coordinates(image, contour)
                robot_square = marker

            if self.__is_a_robot_position_marker__(detected_shape_length, detected_shape_height) and len(approx) > edges['pentagon']:
                marker = utils.find_coordinates(image, contour)
                robot_circle = marker

        return robot_circle, robot_square

    def __is_a_robot_position_marker__(self, detected_shape_length, detected_shape_height):
        ISLAND_MAX_HEIGHT = 100
        ISLAND_MIN_HEIGHT = 10
        ISLAND_MAX_LENGHT = 100
        ISLAND_MIN_LENGHT = 10

        if ISLAND_MIN_HEIGHT < detected_shape_height < ISLAND_MAX_HEIGHT and \
           ISLAND_MIN_LENGHT < detected_shape_length < ISLAND_MAX_LENGHT:
            return True
        else:
            return False

hsv_range = {
    'purple': ((110, 30, 65), (165, 190, 150))
}

edges = {
    'square': 4,
    'pentagon':5
}