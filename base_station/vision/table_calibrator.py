import cv2
import numpy as np
from base_station.vision import vision_utils as utils

class TableCalibrator:
    def __init__(self, shape_detector):
        self.shape_detector = shape_detector

    def get_table_contour(self, image, parameters, opencv = cv2):
        polygonal_approximation_error = parameters['polygonal_approximation_error']

        def approx_polygon(contour):
            return opencv.approxPolyDP(contour, polygonal_approximation_error, True)

        green_contours = self.shape_detector.find_polygon_color(image, 'green_calibration_square', parameters)
        squares = []
        for contour in green_contours:
            if len(approx_polygon(contour)) == 4:
                area = cv2.contourArea(contour)
                squares.append((area, approx_polygon(contour)))

        biggest_square = max(squares, key=lambda item: item[0]) #find biggest square based on area
        leftest_vertex, lowest_vertex, rightest_vertex, upper_vertex = utils.find_shape_height_and_lenght(biggest_square[1])
        pixels_per_meter, top_left_corner, bottom_right_corner = self.__find_table_corners__(leftest_vertex, lowest_vertex, rightest_vertex, upper_vertex)
        table_contour = self.__calculate_table_contour__(top_left_corner, bottom_right_corner)
        print(biggest_square[1])
        image.draw_contours(green_contours)
        image.show()

        return {'pixels_per_meter': pixels_per_meter,
                'table_contour': table_contour}

    def __calculate_table_contour__(self, top_left_corner, bottom_right_corner):
        return np.array([top_left_corner, (bottom_right_corner[0], top_left_corner[1]),
                     bottom_right_corner, (top_left_corner[0], bottom_right_corner[1])])

    def __find_table_corners__(self, leftest_vertex, lowest_vertex, rightest_vertex, upper_vertex):
        detected_shape_length = abs(rightest_vertex - leftest_vertex)
        pixels_per_meter = detected_shape_length / green_square_measurements_in_meters['width']

        top_left_corner = (int(leftest_vertex - pixels_per_meter * green_square_measurements_in_meters['distance_to_left']),
                         int(lowest_vertex - pixels_per_meter * green_square_measurements_in_meters['distance_to_left']))

        bottom_right_corner = (int(rightest_vertex + pixels_per_meter * green_square_measurements_in_meters['distance_to_top']),
                             int(upper_vertex + pixels_per_meter * green_square_measurements_in_meters['distance_to_top']))

        return pixels_per_meter, top_left_corner, bottom_right_corner


hsv_range = {
    'green_calibration_square':  ((40,30,50),  (80,255,255))
}

green_square_measurements_in_meters = {
        'width': 0.663,
        'distance_to_top': 0.225,
        'distance_to_left': 1.42
}

edges = {
    'square' : 4
}