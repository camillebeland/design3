import cv2


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
                    .filter_by_color(hsv_range['purple'])
                    .erode(erode_kernel_size, erode_iterations)
                    .dilate(dilate_kernel_size, dilate_iterations)
                    .find_contours())

        charging_station = {}
        for contour in contours:
            approx = approx_polygon(contour)
            x, y, width, height = cv2.boundingRect(approx)
            print(width)
            print(height)

            if self.__is_a_rectangle__(width, height):
                charging_station = {'x': x + (width/2), 'y': image.get_height() - y}

        return charging_station

    def __is_a_rectangle__(self, width, height):
        aspect_ratio = width / height
        if 0.85 <= aspect_ratio <= 1.15:
            return False
        else:
            return True

hsv_range = {
    'purple': ((110, 30, 65), (165, 190, 190))
}

edges = {
    'rectangle': 4,
}