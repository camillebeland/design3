import cv2
import base_station.vision.vision_utils as utils


class IslandDetector:
    def find_polygon_color(self, image, color, parameters, opencv=cv2):
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
                    .filter_by_color(hsv_range[color])
                    .erode(erode_kernel_size, erode_iterations)
                    .dilate(dilate_kernel_size, dilate_iterations)
                    .find_contours())

        squares, pentagons, triangles, circles = [], [], [], []
        for contour in contours:
            leftest_vertex, lowest_vertex, rightest_vertex, upper_vertex = utils.find_shape_height_and_lenght(contour)
            detected_shape_length = abs(rightest_vertex - leftest_vertex)
            detected_shape_height = abs(upper_vertex - lowest_vertex)
            approx = approx_polygon(contour)

            if self.__is_an_island__(detected_shape_length, detected_shape_height):
                if len(approx) == edges['square'] and self.__is_a_square__(approx):
                    island_square = utils.find_coordinates(image, contour)
                    squares.append(island_square)
                elif len(approx) == edges['triangle']:
                    island_triangle = utils.find_coordinates(image, contour)
                    triangles.append(island_triangle)
                elif len(approx) == edges['pentagon']:
                    island_pentagon = utils.find_coordinates(image, contour)
                    pentagons.append(island_pentagon)
                elif len(approx) > 5:
                    island_circle = utils.find_coordinates(image, contour)
                    circles.append(island_circle)

        return squares, pentagons, triangles, circles

    def __is_a_square__(self, approx):
        x, y, width, height = cv2.boundingRect(approx)
        aspect_ratio = width / height
        if 0.85 <= aspect_ratio <= 1.15:
            return True
        else:
            return False

    def __is_an_island__(self, detected_shape_length, detected_shape_height):
        ISLAND_MAX_HEIGHT = 120
        ISLAND_MIN_HEIGHT = 40
        ISLAND_MAX_LENGHT = 120
        ISLAND_MIN_LENGHT = 40

        if ISLAND_MIN_HEIGHT < detected_shape_height < ISLAND_MAX_HEIGHT and \
           ISLAND_MIN_LENGHT < detected_shape_length < ISLAND_MAX_LENGHT:
            return True
        else:
            return False

hsv_range = {
    'red_lower': ((0, 100, 100), (10, 255, 255)),
    'red_upper': ((160,100,100), (179,255,255)),
    'green': ((40,30,50), (80,255,255)),
    'blue': ((80,50,50), (130,255,255)),
    'yellow': ((17, 70, 90), (33, 255, 255)),
    'purple': ((110, 30, 65), (165, 190, 150))
}

edges = {
    'triangle': 3,
    'square': 4,
    'pentagon': 5,
}