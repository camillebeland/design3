import cv2
import numpy as np
import imutils
from pyimagesearch.shapedetector import ShapeDetector as PolygonDetector


from functools import reduce
class Image:
    def __init__(self, image_src, image_format='bgr',  open_cv=cv2):
        self.__open_cv = open_cv
        self.__image = image_src
        self.__image_format = image_format

    
        
    
    def get_height(self):
        return self.__image.shape[0]
    
    def get_width(self):
        return self.__image.shape[1]
        
    def read_image(self):
        return self.__image

    def __add__(self, other):
        return Image(self.__image + other.__image)

    def filter_median_blur(self, kernel_size=5):
        filtered_image = self.__open_cv.medianBlur(self.__image, kernel_size)
        return Image(filtered_image)

    def filter_gaussian_blur(self, kernel_size, sigmaX):
        filtered_image = self.__open_cv.GaussianBlur(self.__image, kernel_size, sigmaX=sigmaX)
        return Image(filtered_image)

    def filter_by_color(self, hsv_range):
        image = self.__in_hsv()
        masked_image = self.__open_cv.inRange(image.__image, hsv_range[0], hsv_range[1])
        return Image(masked_image, 'gray')

    def canny(self, threshold1, threshold2, apertureSize):
        canny_image = self.__open_cv.Canny(self.__image, threshold1, threshold2, apertureSize)
        return Image(canny_image, 'gray')

    def dilate(self, kernel_size, iterations):
        kernel = np.ones((kernel_size, kernel_size), np.uint8)
        dilated_image = self.__open_cv.dilate(self.__image, kernel, iterations = iterations)
        return Image(dilated_image, 'gray')

    def erode(self, kernel_size, iterations):
        kernel = np.ones((kernel_size, kernel_size), np.uint8)
        eroded_image = self.__open_cv.erode(self.__image, kernel, iterations=iterations)
        return Image(eroded_image, 'gray')

    def find_contours(self):
        contours = self.__open_cv.findContours(self.__image, self.__open_cv.RETR_EXTERNAL, self.__open_cv.CHAIN_APPROX_SIMPLE)
        return contours[0] if imutils.is_cv2() else contours[1]

    def find_hough_circles(self, min_distance, param1, param2, min_radius, max_radius):
        return self.__open_cv.HoughCircles(self.__image, self.__open_cv.HOUGH_GRADIENT, 1, min_distance, param1=param1, param2=param2, minRadius=min_radius, maxRadius=max_radius)

    def __in_hsv(self):
            converted_image = convert[self.__image_format]['hsv'](self.__image)
            return Image(converted_image, 'hsv')

    def __in_bgr(self):
            converted_image = convert[self.__image_format]['bgr'](self.__image)
            return Image(converted_image, 'bgr')

    def show(self):
        image = self.__in_bgr()
        self.__open_cv.imshow('Image',image.__image)
        self.__open_cv.waitKey(0)

    def draw_contours(self, contours):
        img = np.copy(self.__image)
        for contour in contours:
            self.__open_cv.drawContours(img, [contour], -1, (255,0,255),3)
        return Image(img)

		
class TableCalibrator:
    def get_table_calibration(self, image):
	
        blurred_image = image.filter_gaussian_blur((15,15), 0)
        green_contours = (blurred_image
                           .filter_by_color(hsv_range['green_calibration_square'])
                           .erode(5,2)
                           .dilate(5,2)
                           .find_contours())
                          
        biggest_square = 0
        biggest_square_area = 0
        polygon_detector = PolygonDetector()
        for contour in green_contours:
            shape = polygon_detector.detect(contour)
            if shape != "square":
                continue
            area = cv2.contourArea(contour)
            if area >biggest_square_area:
                biggest_square_area = area
                biggest_square = contour
        
        minY = 5000
        maxY = -1
        minX = 5000
        maxX = -1
        
        for vertex in biggest_square:
            if vertex[0][0] < minX:
                minX = vertex[0][0]
            if vertex[0][1] < minY:
                minY = vertex[0][1]
            if vertex[0][0] > maxX:
                maxX = vertex[0][0]
            if vertex[0][1] > maxY:
                maxY =vertex[0][1]
		
        pixelsPerMeter = int(abs(maxX - minX)/0.663)
        topLeftCorner = ((minX+pixelsPerMeter*1.425), (maxY+pixelsPerMeter*0.275))
        bottomRightCorner = ((maxX+pixelsPerMeter*0.275), (minY+pixelsPerMeter*0.275))
        
        return {'pixelsPerMeter': pixelsPerMeter, 'topLeftCorner': topLeftCorner, 'bottomRightCorner': bottomRightCorner}
        
class ShapeDetector:

   

    def find_shapes(self, image, parameters=None):

        blurred_image = image.filter_gaussian_blur((15,15), 0)


        blue_contours = (blurred_image
                         .filter_by_color(hsv_range['blue'])
                         .erode(5,2)
                         .dilate(5,2)
                         .find_contours())

        yellow_contours = (blurred_image
                           .filter_by_color(hsv_range['yellow'])
                           .erode(5,2)
                           .dilate(5,2)
                           .find_contours())

        green_contours = (blurred_image
                          .filter_by_color(hsv_range['green'])
                          .erode(5,2)
                          .dilate(5,2)
                          .find_contours())

        light_red_mask = (blurred_image
                          .filter_by_color(hsv_range['red']))

        dark_red_mask = (blurred_image
                         .filter_by_color(hsv_range['dark_red']))

        light_red_mask.show()

        red_mask = light_red_mask + dark_red_mask

        red_contours = (red_mask
                        .erode(5,2)
                        .dilate(5,2)
                        .find_contours())


        shapes = []

        contours = [red_contours, green_contours, blue_contours, yellow_contours]
        colors = ['red', 'green', 'blue', 'yellow']


        polygon_detector = PolygonDetector()
        for i in [0,1,2,3]:
            colored_contours = contours[i]
            current_color = colors[i]
            for contour in colored_contours:
                shape = polygon_detector.detect(contour)

                minY = 5000
                maxY = -1
                minX = 5000
                maxX = -1

                epsilon = 0.015*cv2.arcLength(contour,True)
                approx = cv2.approxPolyDP(contour,epsilon,True)

                if (not cv2.isContourConvex(approx)):
                    continue

                for vertex in contour:
                    if vertex[0][0] < minX:
                        minX = vertex[0][0]
                    if vertex[0][1] < minY:
                        minY = vertex[0][1]
                    if vertex[0][0] > maxX:
                        maxX = vertex[0][0]
                    if vertex[0][1] > maxY:
                        maxY = vertex[0][1]

                if abs(maxX - minX) > 120:
                    continue
                if abs(maxY - minY) > 120:
                    continue
                if abs(maxX - minX) < 40:
                    continue
                if abs(maxY - minY) < 40:
                    continue

                M = cv2.moments(contour)
                cX = int((M["m10"] / M["m00"]))
                cY = int((M["m01"] / M["m00"]))
                shapes.extend([cX,cY,current_color,shape])
        return shapes



        

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
            return list(map(lambda circle: {'x' : float(circle[0]), 'y' : image.get_height() - float(circle[1]), 'radius' : float(circle[2])}, circles[0,:]))
        else:
            return []

    def find_polygon_color(self, image, polygon, color, parameters, opencv=cv2):
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
            return opencv.approxPolyDP(contour, polygonal_approximation_error , True)

        contours = (image
                    .filter_median_blur(median_blur_kernel_size)
                    .filter_gaussian_blur((gaussian_blur_kernel_size,gaussian_blur_kernel_size),gaussian_blur_sigma_x)
                    .filter_by_color(hsv_range[color])
                    .canny(canny_threshold1,canny_threshold2,canny_aperture_size)
                    .dilate(dilate_kernel_size,dilate_ierations)
                    .erode(erode_kernel_size, erode_iterations)
                    .find_contours())


        return (
            list(
                map(
                    lambda x : {
                        'x' : (reduce(np.add, x)/edges[polygon])[0],
                        'y' : image.get_height() - (reduce(np.add, x)/edges[polygon])[1]
                    },
                    map(
                        lambda x : x[:,0],
                        filter(
                            lambda x: len(x) == edges[polygon],
                            map(approxPolygon, contours)
                        )
                    )
                )
            )
        )

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
    'red' : ((160,180,105), (180,255,255)),
    'dark_red' : ((0,180,100), (20,255,255)),
    'green' : ((50,100,50), (80,255,255)),
    'blue' : ((80,50,50), (130,255,255)),
    'yellow' : ((17,70,90), (33,255,255)),
    "green_calibration_square": ((40,30,50),  (80,255,255))
}

edges = {
    'triangle' : 3,
    'square' : 4,
    'pentagon' : 5,
}
