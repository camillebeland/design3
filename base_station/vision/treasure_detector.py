import cv2
import base_station.vision.vision_utils as utils


class TreasureDetector:
    def __init__(self, shape_detector):
        self.__shape_detector = shape_detector

    def find_treasures(self, image, parameters, opencv=cv2):
        contours = self.__shape_detector.find_polygon_color(image, 'treasure-yellow', parameters)

        treasures = []
        for contour in contours:
            leftest_vertex, lowest_vertex, rightest_vertex, upper_vertex = utils.find_shape_height_and_lenght(contour)
            detected_shape_length = abs(rightest_vertex - leftest_vertex)
            detected_shape_height = abs(upper_vertex - lowest_vertex)
            area = opencv.contourArea(contour)

            if self.__is_a_treasure__(detected_shape_length, detected_shape_height, area):
                treasure = self.__find_treasure_coordinates__(image, contour)
                treasures.append(treasure)
        return treasures

    def __find_treasure_coordinates__(self, image, contour):
        treasure = {}
        moment = cv2.moments(contour)
        center_x = int((moment["m10"] / moment["m00"]))
        centrer_y = int((moment["m01"] / moment["m00"]))
        treasure['x'] = center_x
        treasure['y'] = image.get_height() - centrer_y
        return treasure

    def __is_a_treasure__(self, detected_shape_length, detected_shape_height, area):
        TREASURE_MAX_HEIGHT = 60
        TREASURE_MIN_HEIGHT = 5
        TREASURE_MAX_LENGHT = 60
        TREASURE_MIN_LENGHT = 5
        TREASURE_MAX_AREA = 400
        TREASURE_MIN_AREA = 150

        if TREASURE_MIN_HEIGHT < detected_shape_height < TREASURE_MAX_HEIGHT and \
           TREASURE_MIN_LENGHT < detected_shape_length < TREASURE_MAX_LENGHT and \
           TREASURE_MIN_AREA < area < TREASURE_MAX_AREA:
            return True
        else:
            return False



