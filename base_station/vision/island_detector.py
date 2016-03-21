import cv2
import numpy as np
from functools import reduce


class IslandDetector:
    def __init__(self, shape_detector):
        self.shape_detector = shape_detector

    def find_circle_color(self, image, color, parameters):
        circles = self.shape_detector.find_circle_color(image, color, parameters)
        if circles is not None:
            return list(map(lambda circle: {'x' : float(circle[0]), 'y' : image.get_height() - float(circle[1]), 'radius' : float(circle[2])}, circles[0,:]))
        else:
            return []

    def find_polygon_color(self, image, polygon, color, parameters, opencv=cv2):
        polygonal_approximation_error = parameters['polygonal_approximation_error']

        contours = self.shape_detector.find_polygon_color(image, color, parameters)

        def approx_polygon(contour):
            return opencv.approxPolyDP(contour, polygonal_approximation_error, True)

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
                            map(approx_polygon, contours)
                        )
                    )
                )
            )
        )

hsv_range = {
    'red': ((160,100,100), (179,255,255)),
    'green': ((50,100,50), (80,255,255)),
    'blue': ((80,50,50), (130,255,255)),
    'yellow': ((20,100,100), (30,255,255)),
    'purple': ((110, 30, 65), (165, 190, 150))
}

edges = {
    'triangle': 3,
    'square': 4,
    'pentagon': 5,
}