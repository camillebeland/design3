import cv2
import numpy as np
import base_station.vision.vision_utils as utils

class RobotDetector:
    def find_circle_color(self, image, parameters):
        median_blur_kernel_size = parameters['median_blur_kernel_size']
        gaussian_blur_kernel_size = parameters['gaussian_blur_kernel_size']
        gaussian_blur_sigma_x = parameters['gaussian_blur_sigma_x']
        hough_circle_min_distance = parameters['hough_circle_min_distance']
        hough_circle_param1 = parameters['hough_circle_param1']
        hough_circle_param2 = parameters['hough_circle_param2']
        hough_circle_min_radius = parameters['hough_circle_min_radius']
        hough_circle_max_radius = parameters['hough_circle_max_radius']

        circles = (image
                   .filter_median_blur(median_blur_kernel_size)
                   .filter_by_color(hsv_range['purple'])
                   .filter_gaussian_blur((gaussian_blur_kernel_size, gaussian_blur_kernel_size), gaussian_blur_sigma_x)
                   .find_hough_circles(hough_circle_min_distance,
                                       hough_circle_param1,
                                       hough_circle_param2,
                                       hough_circle_min_radius,
                                       hough_circle_max_radius))
        if(circles is not None):
            return list(map(lambda circle: {'x' : float(circle[0]), 'y' : image.get_height() - float(circle[1]), 'radius' : float(circle[2])}, circles[0,:]))
        else:
            return []

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

        for contour in contours:
            leftest_vertex, lowest_vertex, rightest_vertex, upper_vertex = utils.find_shape_height_and_lenght(contour)
            detected_shape_length = abs(rightest_vertex - leftest_vertex)
            detected_shape_height = abs(upper_vertex - lowest_vertex)
            approx = approx_polygon(contour)

            if self.__is_a_robot_position_marker__(detected_shape_length, detected_shape_height) and len(approx) == edges['square']:
                marker = self.__find_robot_markers_coordinates__(image, contour)
                robot_square = marker

            if self.__is_a_robot_position_marker__(detected_shape_length, detected_shape_height) and len(approx) > edges['pentagon']:
                marker = self.__find_robot_markers_coordinates__(image, contour)
                robot_circle = marker

        return robot_circle, robot_square

    def __find_robot_markers_coordinates__(self, image, contour):
        robot_marker = {}
        moment = cv2.moments(contour)
        center_x = int((moment["m10"] / moment["m00"]))
        centrer_y = int((moment["m01"] / moment["m00"]))
        robot_marker['x'] = center_x
        robot_marker['y'] = image.get_height() - centrer_y
        return robot_marker

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