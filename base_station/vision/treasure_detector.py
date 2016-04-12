import cv2
import base_station.vision.vision_utils as utils


class TreasureDetector:
    def find_treasures(self, image, parameters, opencv=cv2):
        contours = self.__find_contours__(image, 'treasure-yellow', parameters)

        treasures = []
        for contour in contours:
            leftest_vertex, lowest_vertex, rightest_vertex, upper_vertex = utils.find_shape_height_and_lenght(contour)
            detected_shape_length = abs(rightest_vertex - leftest_vertex)
            detected_shape_height = abs(upper_vertex - lowest_vertex)
            area = opencv.contourArea(contour)

            if self.__is_a_treasure__(detected_shape_length, detected_shape_height, area):
                treasure = utils.find_coordinates(image, contour)
                treasures.append(treasure)
        return treasures

    def __find_contours__(self, image, color, parameters):
        blur_kernel_size = parameters['blur_kernel_size']
        erode_kernel_size = parameters['erode_kernel_size']
        erode_iterations = parameters['erode_iterations']
        dilate_kernel_size = parameters['dilate_kernel_size']
        dilate_ierations = parameters['dilate_iterations']

        contours = (image
                    .filter_blur((blur_kernel_size, blur_kernel_size))
                    .filter_by_color(hsv_range[color])
                    .erode(erode_kernel_size, erode_iterations)
                    .dilate(dilate_kernel_size, dilate_ierations)
                    .find_contours())

        return contours

    def __is_a_treasure__(self, detected_shape_length, detected_shape_height, area):
        TREASURE_MAX_HEIGHT = 50
        TREASURE_MIN_HEIGHT = 3
        TREASURE_MAX_LENGHT = 50
        TREASURE_MIN_LENGHT = 3
        TREASURE_MAX_AREA = 400
        TREASURE_MIN_AREA = 100

        if TREASURE_MIN_HEIGHT < detected_shape_height < TREASURE_MAX_HEIGHT and \
           TREASURE_MIN_LENGHT < detected_shape_length < TREASURE_MAX_LENGHT and \
           TREASURE_MIN_AREA < area < TREASURE_MAX_AREA:
            return True
        else:
            return False

hsv_range = {
    'treasure-yellow': ((15, 95, 60), (35, 255, 255))
}

