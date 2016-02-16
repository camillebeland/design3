import cv2
from base_station.world_map_vision.color_ranges import ColorFilter

class CircleFinder(object):
    def __init__(self, image):
        self.image = image


    def find_circle(self):
        origin_image = cv2.imread(self.image)
        median_blurred_image = cv2.medianBlur(origin_image, 3)
        hsv_image = cv2.cvtColor(median_blurred_image, cv2.COLOR_BGR2HSV)

        color_filter = ColorFilter(hsv_image)
        filtered_image = color_filter.all_colors()

        gaussian_image = cv2.GaussianBlur(filtered_image, (9, 9), 2, 2)
        circles = cv2.HoughCircles(gaussian_image, cv2.HOUGH_GRADIENT, 1, len(gaussian_image) / 8,
                                   param1=50, param2=30, minRadius=0, maxRadius=0)

        if(circles is not None):
            for x in circles[0,:]:
                 center_point = (x[0], x[1])
                 radius = x[2]
                 cv2.circle(origin_image, center_point, radius, (0, 255, 0), 2)
                 cv2.circle(origin_image, center_point,2,(0,0,255),3)

        cv2.imshow("Detected red circles on the input image", origin_image)
        cv2.waitKey(0)
        return circles


if __name__ == '__main__':
    circle_finder = CircleFinder(image="circlesImage.jpg")
    circles = circle_finder.find_circle()