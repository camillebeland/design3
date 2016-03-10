from nose.tools import *
from base_station.vision import *

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

hsv_range = {
    'red' : ((160,100,100), (179,255,255)),
    'green' : ((50,100,50), (80,255,255)),
    'blue' : ((80,50,50), (130,255,255)),
    'yellow' : ((20,100,100), (30,255,255))
}

class MockOpenCV:
    def approxPolyDP(curve, epsilon, closed, approxCurve=None):
        return "contours"

class ImageMockCirclesFound:
    def filter_median_blur(self, kernel_size=5):
        return ImageMockCirclesFound()

    def filter_gaussian_blur(self, kernel_size, sigmaX):
        return ImageMockCirclesFound()

    def filter_by_color(self, hsv_range):
        return ImageMockCirclesFound()

    def find_hough_circles(self, min_distance, param1, param2, min_radius, max_radius):
        FOUND_CIRCLES = np.array([[[80.5, 168.5, 14.57738018]]])
        return FOUND_CIRCLES

class ImageMockNoShapeFound:
    def filter_median_blur(self, kernel_size=5):
        return ImageMockNoShapeFound()

    def filter_gaussian_blur(self, kernel_size, sigmaX):
        return ImageMockNoShapeFound()

    def filter_by_color(self, hsv_range):
        return ImageMockNoShapeFound()

    def canny(self, threshold1, threshold2, apertureSize):
        return ImageMockNoShapeFound()

    def dilate(self, kernel_size, iterations):
        return ImageMockNoShapeFound()

    def erode(self, kernel_size, iterations):
        return ImageMockNoShapeFound()

    def find_contours(self):
        return np.array([[[80.5, 168.5, 14.57738018]]])

    def find_hough_circles(self, min_distance, param1, param2, min_radius, max_radius):
        FOUND_CIRCLES = None
        return FOUND_CIRCLES

class TestShapeDetector:
    def setup(self):
        self.image_mock_circle_found = ImageMockCirclesFound()
        self.image_mock_shapes_not_found = ImageMockNoShapeFound()
        self.shape_detector = ShapeDetector()

    def test_find_blue_circle_with_blue_circles_should_return_circles(self):
        circles = self.shape_detector.find_circle_color(self.image_mock_circle_found, 'blue', test_polygon_params)
        PARSED_FOUND_CIRCLES = [{'radius': 14.57738018, 'y': 168.5, 'x': 80.5}]
        assert_equal(PARSED_FOUND_CIRCLES, circles)

    def test_find_blue_circle_without_circles_should_return_no_circles(self):
        circles = self.shape_detector.find_circle_color(self.image_mock_shapes_not_found, 'blue', test_polygon_params)
        PARSED_CIRCLES_FOUND = []
        assert_equal(PARSED_CIRCLES_FOUND, circles)

    def test_find_triangle_blue_with_no_polygons_should_return_no_triangles(self):
        triangles = self.shape_detector.find_polygon_color(self.image_mock_shapes_not_found, 'triangle', 'blue', test_polygon_params, MockOpenCV())
        PARSED_TRIANGLES_FOUND = []
        assert_equal(triangles, PARSED_TRIANGLES_FOUND)

