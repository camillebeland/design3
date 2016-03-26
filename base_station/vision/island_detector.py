import cv2
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

        squares, pentagons, triangles = [], [], []
        for contour in contours:
            leftest_vertex, lowest_vertex, rightest_vertex, upper_vertex = utils.find_shape_height_and_lenght(contour)
            detected_shape_length = abs(rightest_vertex - leftest_vertex)
            detected_shape_height = abs(upper_vertex - lowest_vertex)
            approx = approx_polygon(contour)

            if self.__is_an_island__(detected_shape_length, detected_shape_height):
                if len(approx) == edges['square']:
                    island_square = self.__find_island_coordinates__(image, contour)
                    squares.append(island_square)
                elif len(approx) == edges['triangle']:
                    island_triangle = self.__find_island_coordinates__(image, contour)
                    triangles.append(island_triangle)
                elif len(approx) == edges['pentagon']:
                    island_pentagon = self.__find_island_coordinates__(image, contour)
                    pentagons.append(island_pentagon)

        return squares, pentagons, triangles

    def __find_island_coordinates__(self, image, contour):
        island = {}
        moment = cv2.moments(contour)
        center_x = int((moment["m10"] / moment["m00"]))
        centrer_y = int((moment["m01"] / moment["m00"]))
        island['x'] = center_x
        island['y'] = image.get_height() - centrer_y
        return island

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
    'red': ((160,100,100), (179,255,255)),
    'green': ((50,100,50), (80,255,255)),
    'blue': ((80,50,50), (130,255,255)),
    'yellow': ((17,70,90), (33,255,255)),
    'purple': ((110, 30, 65), (165, 190, 150))
}

edges = {
    'triangle': 3,
    'square': 4,
    'pentagon': 5,
}