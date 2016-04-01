import cv2
import numpy as np

class ImageWrapper:
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

    def filter_median_blur(self, kernel_size=5):
        filtered_image = self.__open_cv.medianBlur(self.__image, kernel_size)
        return ImageWrapper(filtered_image)

    def filter_gaussian_blur(self, kernel_size, sigmaX):
        filtered_image = self.__open_cv.GaussianBlur(self.__image, kernel_size, sigmaX=sigmaX)
        return ImageWrapper(filtered_image)

    def filter_by_color(self, hsv_range):
        image = self.__in_hsv()
        masked_image = self.__open_cv.inRange(image.__image, hsv_range[0], hsv_range[1])
        return ImageWrapper(masked_image, 'gray')

    def canny(self, threshold1, threshold2, apertureSize):
        canny_image = self.__open_cv.Canny(self.__image, threshold1, threshold2, apertureSize)
        return ImageWrapper(canny_image, 'gray')

    def dilate(self, kernel_size, iterations):
        kernel = np.ones((kernel_size, kernel_size), np.uint8)
        dilated_image = self.__open_cv.dilate(self.__image, kernel, iterations = iterations)
        return ImageWrapper(dilated_image, 'gray')

    def erode(self, kernel_size, iterations):
        kernel = np.ones((kernel_size, kernel_size), np.uint8)
        eroded_image = self.__open_cv.erode(self.__image, kernel, iterations=iterations)
        return ImageWrapper(eroded_image, 'gray')

    def find_contours(self):
        img, contours, hierarchy = self.__open_cv.findContours(self.__image, self.__open_cv.RETR_LIST, self.__open_cv.CHAIN_APPROX_SIMPLE)
        return contours

    def find_hough_circles(self, min_distance, param1, param2, min_radius, max_radius):
        return self.__open_cv.HoughCircles(self.__image, self.__open_cv.HOUGH_GRADIENT, 1, min_distance, param1=param1, param2=param2, minRadius=min_radius, maxRadius=max_radius)

    def __in_hsv(self):
            converted_image = convert[self.__image_format]['hsv'](self.__image)
            return ImageWrapper(converted_image, 'hsv')

    def __in_bgr(self):
            converted_image = convert[self.__image_format]['bgr'](self.__image)
            return ImageWrapper(converted_image, 'bgr')

    def show(self):
        image = self.__in_bgr()
        self.__open_cv.imshow('Image',image.__image)
        self.__open_cv.waitKey(0)
        return ImageWrapper(image)

    def draw_circles(self, circles):
        img = np.copy(self.__image)
        for circle in circles:
            center = (int(circle['x']), int(circle['y']))
            radius = int(circle['radius'])
            self.__open_cv.circle(img, center, radius, (0,255,255),3)
        return ImageWrapper(img)

    def draw_contours(self, contours):
        img = np.copy(self.__image)
        for contour in contours:
            self.__open_cv.drawContours(img, [contour], -1, (255,0,255),3)
        return ImageWrapper(img)

    def mask_image(self, contour):
        img = np.copy(self.__image)
        blank_image = np.zeros((self.get_height(),self.get_width()), np.uint8)
        mask = cv2.fillPoly(blank_image, pts =[contour], color=(255,255,255))
        mask = cv2.dilate(mask , None, iterations=int(40*((self.get_height()/1200)**2)))
        img = cv2.bitwise_and(img, img, mask=mask)
        return ImageWrapper(img)

    def mask_image_embedded(self, contour):
        img = np.copy(self.__image)
        blank_image = np.zeros((self.get_height(),self.get_width()), np.uint8)
        mask = cv2.fillPoly(blank_image, pts =[contour], color=(255,255,255))
        img = cv2.bitwise_and(img, img, mask=mask)
        return ImageWrapper(img)

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