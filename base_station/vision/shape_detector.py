import cv2
import numpy as np
from functools import reduce


class ShapeDetector:
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

        return circles

    def find_polygon_color(self, image, color, parameters):
        median_blur_kernel_size = parameters['median_blur_kernel_size'] 
        gaussian_blur_kernel_size = parameters['gaussian_blur_kernel_size']
        gaussian_blur_sigma_x = parameters['gaussian_blur_sigma_x']
        canny_threshold1 = parameters['canny_threshold1']
        canny_threshold2 = parameters['canny_threshold2']
        canny_aperture_size = parameters['canny_aperture_size']
        dilate_kernel_size = parameters['dilate_kernel_size']
        dilate_ierations = parameters['dilate_ierations']
        erode_kernel_size = parameters['erode_kernel_size']
        erode_iterations = parameters['erode_iterations']

        contours = (image
                    .filter_median_blur(median_blur_kernel_size)
                    .filter_gaussian_blur((gaussian_blur_kernel_size,gaussian_blur_kernel_size),gaussian_blur_sigma_x)
                    .filter_by_color(hsv_range[color])
                    .canny(canny_threshold1,canny_threshold2,canny_aperture_size)
                    .dilate(dilate_kernel_size,dilate_ierations)
                    .erode(erode_kernel_size, erode_iterations)
                    .find_contours())

        return contours

hsv_range = {
    'red': ((160,100,100), (179,255,255)),
    'green': ((50,100,50), (80,255,255)),
    'blue': ((80,50,50), (130,255,255)),
    'yellow': ((20,100,100), (30,255,255)),
    'purple': ((110, 30, 65), (165, 190, 150)),
    'green_calibration_square':  ((40,30,50),  (80,255,255)),
    'treasure-yellow': ((15,80,70), (35,255,255))
}

edges = {
    'triangle': 3,
    'square': 4,
    'pentagon': 5,
}
