import cv2
import numpy as np

class Image:
    def __init__(self, image_src, image_format='bgr'):
        self.__image = image_src
        self.__image_format = image_format

    def filter_median_blur(self, kernel_size=5):
        filtered_image = cv2.medianBlur(self.__image, kernel_size)
        return Image(filtered_image)

    def filter_gaussian_blur(self, kernel_size, sigmaX):
        filtered_image = cv2.GaussianBlur(self.__image, kernel_size, sigmaX=sigmaX)
        return Image(filtered_image)

    def filter_by_color(self, hsv_range):
        image = self.__in_hsv()
        masked_image = cv2.inRange(image.__image, hsv_range[0], hsv_range[1])
        return Image(masked_image, 'gray')

    def canny(self, threshold1, threshold2, apertureSize):
        canny_image = cv2.Canny(self.__image, threshold1, threshold2, apertureSize)
        return Image(canny_image, 'gray')

    def dilate(self, kernel_size, iterations):
        kernel = np.ones((kernel_size, kernel_size), np.uint8)
        dilated_image = cv2.dilate(self.__image, kernel, iterations = iterations)
        return Image(dilated_image, 'gray')

    def erode(self, kernel_size, iterations):
        kernel = np.ones((kernel_size, kernel_size), np.uint8)
        eroded_image = cv2.erode(self.__image, kernel, iterations=iterations)
        return Image(eroded_image, 'gray')

    def find_contours(self):
        img, contours, hierarchy = cv2.findContours(self.__image, cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)
        return contours

    def find_hough_circles(self, min_distance, param1, param2, min_radius, max_radius):
        return cv2.HoughCircles(self.__image, cv2.HOUGH_GRADIENT, 1, min_distance, param1=param1, param2=param2, minRadius=min_radius, maxRadius=max_radius)

    def __in_hsv(self):
            converted_image = convert[self.__image_format]['hsv'](self.__image)
            return Image(converted_image, 'hsv')

    def __in_bgr(self):
            converted_image = convert[self.__image_format]['bgr'](self.__image)
            return Image(converted_image, 'bgr')

    def show(self):
        image = self.__in_bgr()
        cv2.imshow('Image',image.__image)
        cv2.waitKey(0)

    def draw_contours(self, contours):
        img = np.copy(self.__image)
        cv2.drawContours(img, contours, -1, (255,0,0), 3)
        return Image(img)

    def draw_circles(self, circles):
        img = np.copy(self.__image)
        for circle in circles:
            center = (int(circle['x']), int(circle['y']))
            radius = int(circle['radius'])
            cv2.circle(img, center, radius, (0,255,255),3)
        return Image(img)

class ShapeDetector:
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
        if(circles is not None):
            return list(map(lambda circle: {'x' : float(circle[0]), 'y' : float(circle[1]), 'radius' : float(circle[2])}, circles[0,:]))
        else:
            return []


    def find_polygon_color(self, image, polygon, color, parameters):
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
            return cv2.approxPolyDP(contour, polygonal_approximation_error , True)

        contours = (image
                    .filter_median_blur(median_blur_kernel_size)
                    .filter_gaussian_blur((gaussian_blur_kernel_size,gaussian_blur_kernel_size),gaussian_blur_sigma_x)
                    .filter_by_color(hsv_range[color])
                    .canny(canny_threshold1,canny_threshold2,canny_aperture_size)
                    .dilate(dilate_kernel_size,dilate_ierations)
                    .erode(erode_kernel_size, erode_iterations)
                    .find_contours())


        return (list(filter(lambda x: len(x) == edges[polygon], map(approxPolygon, contours))))

convert = {
    'bgr' : {
        'hsv' : lambda image : cv2.cvtColor(image, cv2.COLOR_BGR2HSV),
        'gray' : lambda image : cv2.cvtColor(image, cv2.COLOR_BGR2GRAY),
        'bgr' : lambda image : image

    },
    'hsv' : {
        'bgr' : lambda image : cv2.cvtColor(image, cv2.COLOR_HSV2BGR),
        'gray' : lambda image : cv2.cvtColor(
            cv2.cvtColor(image, cv2.COLOR_HSV2BGR), cv2.COLOR_BGR2GRAY
        ),
        'hsv' : lambda image : image
    },
    'gray' : {
        'bgr' : lambda image : image
    }
}

hsv_range = {
    'red' : ((160,100,100), (179,255,255)),
    'green' : ((50,100,50), (80,255,255)),
    'blue' : ((80,50,50), (130,255,255)),
    'yellow' : ((20,100,100), (30,255,255))
}

edges = {
    'triangle' : 3,
    'square' : 4,
    'pentagon' : 5,
}

default_camille_polygon_params = {
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
    'polygonal_approximation_error' : 4
}
