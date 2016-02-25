import cv2
import numpy

def angle_cos(p0, p1, p2):
    d1, d2 = (p0 - p1).astype('float'), (p2 - p1).astype('float')
    return abs(numpy.dot(d1, d2) / numpy.sqrt(numpy.dot(d1, d1) * numpy.dot(d2, d2)))


def median_blur_filter(image):
    return cv2.medianBlur(image, ksize=3)


def convert_color_to_hsv(image):
    return cv2.cvtColor(image, cv2.COLOR_BGR2HSV)

def convert_color_to_bgr(image):
    return cv2.cvtColor(image, cv2.COLOR_HSV2BGR)

def convert_color_to_black_white(image):
    return cv2.cvtColor(image, cv2.COLOR_RGB2GRAY)

def gaussian_blur(image):
    return cv2.GaussianBlur(image, (5, 5), 0)


def gaussian_blur_circles(image):
    return cv2.GaussianBlur(image, (9, 9), 2, 2)


def split(image):
    return cv2.split(image)


def canny(image):
    return cv2.Canny(image, 0, 50, apertureSize=5)


def dilate(image):
    return cv2.dilate(image, kernel=numpy.ones((5,5),numpy.uint8), iterations=10)


def erode(image):
    return cv2.erode(image, kernel=numpy.ones((99,99),numpy.uint8), iterations=10)


def threshold(image, threshold):
    retval, image = cv2.threshold(image, threshold, 255, cv2.THRESH_BINARY)
    return image


def find_contours(image):
    bin, contours, hierarchy = cv2.findContours(image, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    return contours


def find_circles(image):
    return cv2.HoughCircles(image, cv2.HOUGH_GRADIENT, 1, len(image) / 8, param1=50, param2=30, minRadius=0, maxRadius=0)


def arc_length(contour):
    return cv2.arcLength(contour, True)


def approx_polygon_curve(contour, contour_length):
    return cv2.approxPolyDP(contour, 0.02 * contour_length, True)


def is_triangle(contour):
    return len(contour) == 3 and cv2.contourArea(contour) < 1500 and cv2.isContourConvex(contour)


def is_pentagon(contour):
    return len(contour) == 5 and cv2.contourArea(contour) > 1500 and cv2.isContourConvex(contour)


def is_square(contour):
    return len(contour) == 4 and cv2.contourArea(contour) > 1500 and cv2.isContourConvex(contour)