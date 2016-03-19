import cv2


class TreasureDetector:
    def find_treasures(self, image, parameters, opencv=cv2):
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
        polygonal_approximation_error = parameters['polygonal_approximation_error']

        def approxPolygon(contour):
            return opencv.approxPolyDP(contour, polygonal_approximation_error, True)

        contours = (image
                    .filter_median_blur(median_blur_kernel_size)
                    .filter_gaussian_blur((gaussian_blur_kernel_size,gaussian_blur_kernel_size),gaussian_blur_sigma_x)
                    .filter_by_color(hsv_range['yellow'])
                    .canny(canny_threshold1,canny_threshold2,canny_aperture_size)
                    .dilate(dilate_kernel_size,dilate_ierations)
                    .erode(erode_kernel_size, erode_iterations)
                    .find_contours())

        treasures = []
        for contour in contours:
            detected_shape_length, detected_shape_height= self.__find_shape_height_and_lenght__(contour)
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

    def __find_shape_height_and_lenght__(self, contour):
        leftest_vertex = min([vertex[0][0] for vertex in contour])
        lowest_vertex = min([vertex[0][1] for vertex in contour])
        rightest_vertex = max([vertex[0][0] for vertex in contour])
        upper_vertex = max([vertex[0][1] for vertex in contour])

        detected_shape_length = abs(rightest_vertex - leftest_vertex)
        detected_shape_height = abs(upper_vertex - lowest_vertex)

        return detected_shape_height, detected_shape_length

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

hsv_range = {
    'yellow': ((15,80,70), (35,255,255))
}



