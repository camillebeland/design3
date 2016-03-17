import cv2
import numpy as np
import imutils
from pyimagesearch.shapedetector import ShapeDetector as PolygonDetector
from vision import *

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
        
        pixelsPerMeter = int(abs(maxX - minX)/greenSquareWidth)
        topLeftCorner = (int(minX-pixelsPerMeter*greenSquareToLeft), int(minY-pixelsPerMeter*greenSquareToTop))
        bottomRightCorner = (int(maxX+pixelsPerMeter*greenSquareToTop), int(maxY+pixelsPerMeter*greenSquareToTop))
        
        return {'pixelsPerMeter': pixelsPerMeter, 'tableContour': np.array([topLeftCorner,(bottomRightCorner[0],
		topLeftCorner[1]),bottomRightCorner,(topLeftCorner[0], bottomRightCorner[1])])}
 
greenSquareWidth = 0.663 #meters
greenSquareToTop = 0.225 # meters
greenSquareToLeft = 1.42 # meters
 