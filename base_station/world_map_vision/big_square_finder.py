import numpy
import base_station.world_map_vision.opencv_vision_wrapper as vision_wrapper
from base_station.world_map_vision.color_filter import *

class BigSquareFinder(object):
    def __init__(self, image, color_filter):
        self.image = image
        self.origin_image = image
        self.color_filter = color_filter

    def find_big_square(self):
        squares = []
        pentagons = []
        triangles = []

        self.image = vision_wrapper.median_blur_filter(self.image)
        self.image = vision_wrapper.convert_color(self.image)
        color_filtered_image = self.color_filter.range(self.image)
        gaussian_blurred_image = vision_wrapper.gaussian_blur(color_filtered_image)

        for gray in vision_wrapper.split(gaussian_blurred_image):
            for threshold in range(0, 255, 26):
                if threshold == 0:
                    contour_image = vision_wrapper.canny(gray)
                    contour_image = vision_wrapper.dilate(contour_image)
                else:
                    contour_image = vision_wrapper.threshold(gray, threshold)

                contours = vision_wrapper.find_contours(contour_image)
                for contour in contours:
                    contour_length = vision_wrapper.arc_length(contour)
                    contour = vision_wrapper.approx_polygon_curve(contour, contour_length)
                    if vision_wrapper.is_triangle(contour):
                        triangles.append(contour)
                    if vision_wrapper.is_pentagon(contour):
                        pentagons.append(contour)
                    if vision_wrapper.is_square(contour):
                        contour = contour.reshape(-1, 2)
                        max_cos = numpy.max([vision_wrapper.angle_cos(contour[i], contour[(i + 1) % 4], contour[(i + 2) % 4]) for i in range(4)])
                        if max_cos < 0.1:
                            squares.append(contour)

        gaussian_blurred_image = vision_wrapper.gaussian_blur_circles(color_filtered_image)
        circles = vision_wrapper.find_circles(gaussian_blurred_image)

        return circles, triangles, squares, pentagons

    def draw_contours(self, circles, triangles, squares, pentagons, origin_image):
        if(circles is not None):
            for x in circles[0,:]:
                 center_point = (x[0], x[1])
                 radius = x[2]
                 cv2.circle(origin_image, center_point, radius, (0, 255, 255), 2)
                 cv2.circle(origin_image, center_point,2,(0, 0 ,255),3)

        cv2.drawContours(origin_image, squares, -1, (0, 255, 0), 3) #green
        cv2.drawContours(origin_image, triangles, -1, (255, 0, 0), 3) #blue
        cv2.drawContours(origin_image, pentagons, -1, (0, 0, 255), 3) #red

if __name__ == '__main__':
    img = cv2.imread("all_red.jpg")
    island_finder = IslandsFinder(img, AllColorFilter())
    circles, triangles, squares, pentagons = island_finder.find_islands()
    island_finder.draw_contours(circles, triangles, squares, pentagons, img)
    cv2.imshow('islands', img)
    ch = 0xFF & cv2.waitKey()
    cv2.destroyAllWindows()
