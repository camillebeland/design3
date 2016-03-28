import cv2
import base_station.vision.vision_utils as utils

class ChargingStationDetector:
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
                    .filter_by_color(hsv_range['blue'])
                    .erode(erode_kernel_size, erode_iterations)
                    .dilate(dilate_kernel_size, dilate_iterations)
                    .find_contours())

        charging_station = {}
        for contour in contours:
            leftest_vertex, lowest_vertex, rightest_vertex, upper_vertex = utils.find_shape_height_and_lenght(contour)
            detected_shape_length = abs(rightest_vertex - leftest_vertex)
            detected_shape_height = abs(upper_vertex - lowest_vertex)
            approx = approx_polygon(contour)

            if self.__is_charging_station__(detected_shape_length, detected_shape_height):
                if len(approx) == edges['rectangle'] and self.__is_a_rectangle__(approx):
                    charging_station = utils.find_coordinates(image, contour)

        return charging_station

    def __is_a_rectangle__(self, approx):
        x, y, width, height = cv2.boundingRect(approx)
        aspect_ratio = width / height
        if 0.85 <= aspect_ratio <= 1.15:
            return False
        else:
            return True

    def __is_charging_station__(self, detected_shape_length, detected_shape_height):
        CHARGING_STATION_MAX_HEIGHT = 120
        CHARGING_STATION_MIN_HEIGHT = 40
        CHARGING_STATION_MAX_LENGHT = 120
        CHARGING_STATION_MIN_LENGHT = 40

        if CHARGING_STATION_MIN_HEIGHT < detected_shape_height < CHARGING_STATION_MAX_HEIGHT and \
           CHARGING_STATION_MIN_LENGHT < detected_shape_length < CHARGING_STATION_MAX_LENGHT:
            return True
        else:
            return False

hsv_range = {
    'blue': ((80,50,50), (130,255,255))
}

edges = {
    'rectangle': 4,
}