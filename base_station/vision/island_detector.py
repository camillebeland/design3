import cv2
import numpy as np
from functools import reduce
import base_station.vision.vision_utils as utils

class IslandDetector:
    def find_circle_color(self, image, color, parameters):
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
                   .filter_by_color(hsv_range[color])
                   .filter_gaussian_blur((gaussian_blur_kernel_size, gaussian_blur_kernel_size), gaussian_blur_sigma_x)
                   .find_hough_circles(hough_circle_min_distance,
                                       hough_circle_param1,
                                       hough_circle_param2,
                                       hough_circle_min_radius,
                                       hough_circle_max_radius))

        if circles is not None:
            return list(map(lambda circle: {'x' : float(circle[0]), 'y' : image.get_height() - float(circle[1]), 'radius' : float(circle[2])}, circles[0,:]))
        else:
            return []

    def find_polygon_color(self, image, polygon, color, parameters, opencv=cv2):
        median_blur_kernel_size = parameters['median_blur_kernel_size']
        erode_kernel_size = parameters['erode_kernel_size']
        erode_iterations = parameters['erode_iterations']
        dilate_kernel_size = parameters['dilate_kernel_size']
        dilate_iterations = parameters['dilate_iterations']


        def approx_polygon(contour):
            epsilon = 0.02*cv2.arcLength(contour, True)
            return opencv.approxPolyDP(contour, epsilon, True)

        contours = (image
                    .filter_median_blur(median_blur_kernel_size)
                    .filter_by_color(hsv_range[color])
                    .dilate(dilate_kernel_size, dilate_iterations)
                    .erode(erode_kernel_size, erode_iterations)
                    .find_contours())

        islands = []
        for contour in contours:
            leftest_vertex, lowest_vertex, rightest_vertex, upper_vertex = utils.find_shape_height_and_lenght(contour)
            detected_shape_length = abs(rightest_vertex - leftest_vertex)
            detected_shape_height = abs(upper_vertex - lowest_vertex)
            area = opencv.contourArea(contour)
            approx = approx_polygon(contour)

            if self.__is_an_island__(detected_shape_length, detected_shape_height, area) and len(approx) == edges[polygon]:
                treasure = self.__find_island_coordinates__(image, contour)
                islands.append(treasure)

        return islands

    def __find_island_coordinates__(self, image, contour):
        island = {}
        moment = cv2.moments(contour)
        center_x = int((moment["m10"] / moment["m00"]))
        centrer_y = int((moment["m01"] / moment["m00"]))
        island['x'] = center_x
        island['y'] = image.get_height() - centrer_y
        return island

    def __is_an_island__(self, detected_shape_length, detected_shape_height, area):
        ISLAND_MAX_HEIGHT = 160
        ISLAND_MIN_HEIGHT = 50
        ISLAND_MAX_LENGHT = 160
        ISLAND_MIN_LENGHT = 50
        ISLAND_MAX_AREA = 5000
        ISLAND_MIN_AREA = 2000

        if ISLAND_MIN_HEIGHT < detected_shape_height < ISLAND_MAX_HEIGHT and \
           ISLAND_MIN_LENGHT < detected_shape_length < ISLAND_MAX_LENGHT and \
           ISLAND_MIN_AREA < area < ISLAND_MAX_AREA:
            return True
        else:
            return False

hsv_range = {
    'red': ((160,100,100), (179,255,255)),
    'green': ((50,100,50), (80,255,255)),
    'blue': ((80,50,50), (130,255,255)),
    'yellow': ((20,100,100), (30,255,255)),
    'purple': ((110, 30, 65), (165, 190, 150))
}

edges = {
    'triangle': 3,
    'square': 4,
    'pentagon': 5,
}