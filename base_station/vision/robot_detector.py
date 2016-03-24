import cv2
import numpy as np
from functools import reduce
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

        if circles is not None:
            return list(map(lambda circle: {'x' : float(circle[0]), 'y' : image.get_height() - float(circle[1]), 'radius' : float(circle[2])}, circles[0,:]))
        else:
            return []

    def find_polygon_color(self, image, parameters, opencv=cv2):
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
                    .filter_by_color(hsv_range['purple'])
                    .dilate(dilate_kernel_size, dilate_iterations)
                    .erode(erode_kernel_size, erode_iterations)
                    .find_contours())

        return (
                list(
                    map(
                        lambda x : {
                            'x' : (reduce(np.add, x)/edges['square'])[0],
                            'y' : image.get_height() - (reduce(np.add, x)/edges['square'])[1]
                        },
                        map(
                            lambda x : x[:,0],
                            filter(
                                lambda x: len(x) == edges['square'],
                                map(approx_polygon, contours)
                            )
                        )
                    )
                )
            )

hsv_range = {
    'purple': ((110, 30, 65), (165, 190, 150))
}

edges = {
    'square' : 4
}