import cv2
import numpy as np
from functools import reduce


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


        contours = (image
                    .filter_median_blur(median_blur_kernel_size)
                    .filter_by_color(hsv_range[color])
                    .dilate(dilate_kernel_size, dilate_iterations)
                    .erode(erode_kernel_size, erode_iterations)
                    .find_contours())

        def approx_polygon(contour):
            epsilon = 0.02*opencv.arcLength(contour, True)
            return opencv.approxPolyDP(contour, epsilon, True)

        return (
            list(
                map(
                    lambda x : {
                        'x' : (reduce(np.add, x)/edges[polygon])[0],
                        'y' : image.get_height() - (reduce(np.add, x)/edges[polygon])[1]
                    },
                    map(
                        lambda x : x[:,0],
                        filter(
                            lambda x: len(x) == edges[polygon],
                            map(approx_polygon, contours)
                        )
                    )
                )
            )
        )

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