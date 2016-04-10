import numpy as np
from nose.tools import *

from vision_utils.image_wrapper import ImageWrapper

test_polygon_params = {
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
    'polygonal_approximation_error' : 4,
    'hough_circle_min_distance' : 50,
    'hough_circle_param1' : 50,
    'hough_circle_param2' : 30,
    'hough_circle_min_radius' : 0,
    'hough_circle_max_radius' : 0
}

class MockOpenCV:
    RETR_LIST = "RETR_LIST"
    CHAIN_APPROX_SIMPLE = "CHAIN_APPROX_SIMPLE"
    HOUGH_GRADIENT = "HOUGH_GRADIENT"

    def medianBlur(self, image, kernel_size):
        return "median_blurred_image"

    def GaussianBlur(self, image, kernel_size, sigmaX):
        return "gaussian_blurred_image"

    def Canny(self, image, threshold1, threshold2, apertureSize):
        return "canny_contoured_image"

    def erode(self, image, kernel, iterations):
        return "eroded_image"

    def dilate(self, image, kernel, iterations):
        return "dilated_image"

    def findContours(self, image, mode, method):
        return "img", "contours", "hierarchy"

    def HoughCircles(self, image, method, dp, minDist, param1, param2, minRadius, maxRadius):
        return "circles"

vision = ImageWrapper(np.array(1), open_cv=MockOpenCV())

def test_given_an_image_when_median_blur_median_blurred_image_returned():
    image = vision.filter_median_blur(test_polygon_params['median_blur_kernel_size'])
    assert_equal("median_blurred_image", image.read_image())

def test_given_an_image_when_gaussian_blurred_gaussian_blurred_image_returned():
    image = vision.filter_gaussian_blur(test_polygon_params['gaussian_blur_kernel_size'], test_polygon_params['gaussian_blur_sigma_x'])
    assert_equal("gaussian_blurred_image", image.read_image())

def test_given_an_image_when_filter_by_color_filtered_by_color_image_returned():
    image = vision.canny(test_polygon_params['canny_threshold1'], test_polygon_params['canny_threshold2'], test_polygon_params['canny_aperture_size'])
    assert_equal("canny_contoured_image", image.read_image())

def test_given_an_image_when_dilate_dilated_image_returned():
    image = vision.dilate(test_polygon_params['dilate_kernel_size'], test_polygon_params['dilate_ierations'])
    assert_equal("dilated_image", image.read_image())

def test_given_an_image_when_erode_eroded_image_returned():
    image = vision.erode(test_polygon_params['erode_kernel_size'], test_polygon_params['erode_iterations'])
    assert_equal("eroded_image", image.read_image())

def test_given_an_image_when_find_contour_contours_returned():
    contours = vision.find_contours()
    assert_equal("contours", contours)

def test_given_an_image_when_find_circles_circles_returned():
    circles = vision.find_hough_circles(test_polygon_params['hough_circle_min_distance'], test_polygon_params['hough_circle_param1'],
                                         test_polygon_params['hough_circle_param2'], test_polygon_params['hough_circle_min_radius'],
                                         test_polygon_params['hough_circle_max_radius'])
    assert_equal("circles", circles)
