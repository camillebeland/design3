import numpy as np
from base_station.pyimagesearch.shapedetector import ShapeDetector as PolygonDetector
from functools import reduce
from base_station.image_wrapper import ImageWrapper
import sys
import cv2

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
        red_mask = light_red_mask + dark_red_mask
        red_contours = (red_mask
                        .erode(5,2)
                        .dilate(5,2)
                        .find_contours())
        shapes = []
        contours = [red_contours, green_contours, blue_contours, yellow_contours]
        colors = ['red', 'green', 'blue', 'yellow']
        polygon_detector = PolygonDetector()
        for i in [0,1,2,3]: #pour toutes les couleurs
            colored_contours = contours[i]
            current_color = colors[i]
            for contour in colored_contours: #pour chaque contour trouvé
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

                moments = cv2.moments(contour)
                cX = int((moments["m10"] / moments["m00"]))
                cY = int((moments["m01"] / moments["m00"]))
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

    def find_polygon_color_remi(self, image, polygon, color, parameters, opencv=cv2):
        gaussian_blur_kernel_size = parameters['gaussian_blur_kernel_size']
        gaussian_blur_sigma_x = parameters['gaussian_blur_sigma_x']
        dilate_kernel_size = parameters['dilate_kernel_size']
        dilate_ierations = parameters['dilate_ierations']
        erode_kernel_size = parameters['erode_kernel_size']
        erode_iterations = parameters['erode_iterations']
        shape_min_height = parameters['shape_min_height']
        shape_max_height = parameters['shape_max_height']
        shape_min_width = parameters['shape_min_width']
        shape_max_width = parameters['shape_max_width']
        polygonal_approximation_error = parameters['polygonal_approximation_error']

        def approxPolygon(contour):
            islands = []
            epsilon = polygonal_approximation_error * opencv.arcLength(contour,True)
            approx = opencv.approxPolyDP(contour, epsilon, True)

            if shape_is_contained_within(contour, shape_max_height, shape_max_width, shape_min_height, shape_min_width)\
                    and opencv.isContourConvex(approx):
                islands.extend(contour)

            return islands

        contours = (image
                    .filter_gaussian_blur((gaussian_blur_kernel_size,gaussian_blur_kernel_size),gaussian_blur_sigma_x)
                    .filter_by_color(hsv_range[color])
                    .erode(erode_kernel_size, erode_iterations)
                    .dilate(dilate_kernel_size,dilate_ierations)
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


def shape_is_contained_within(shape_contour, max_height, max_width, min_height, min_width):
        is_contained_within = True
        lowest_vertex = sys.maxsize
        highest_vertex = -1
        leftest_vertex = sys.maxsize
        rightest_vertex = -1

        for vertex in shape_contour:
            if vertex[0][0] < leftest_vertex:
                leftest_vertex = vertex[0][0]
            if vertex[0][1] < lowest_vertex:
                lowest_vertex = vertex[0][1]
            if vertex[0][0] > rightest_vertex:
                rightest_vertex = vertex[0][0]
            if vertex[0][1] > highest_vertex:
                highest_vertex = vertex[0][1]

        if (abs(rightest_vertex - leftest_vertex) > max_width or
            abs(highest_vertex - lowest_vertex) > max_height or
            abs(rightest_vertex - leftest_vertex) < min_width or
            abs(highest_vertex - lowest_vertex) < min_height):
            is_contained_within = False

        return is_contained_within

hsv_range = {
    'red' : ((160,180,105), (180,255,255)),
    'dark_red' : ((0,180,100), (20,255,255)),
    'green' : ((50,100,50), (80,255,255)),
    'blue' : ((80,50,50), (130,255,255)),
    'yellow' : ((17,70,90), (33,255,255))
}

edges = {
    'triangle' : 3,
    'square' : 4,
    'pentagon' : 5,
}


if __name__ == "__main__":
    import cv2
    image = cv2.imread("mock_image.jpg")
    image = ImageWrapper(image)
    shapes = ShapeDetector()
    shapes = shapes.find_shapes(image)
    print(shapes)