import cv2

class ColorFilter:
    def __init__(self, image):
        self.image = image

    def red_range(self):
        lower_red_hue_range = cv2.inRange(self.image, (0, 100, 100), (10, 255, 255))
        upper_red_hue_range = cv2.inRange(self.image, (160, 100, 100), (179, 255, 255))
        red_hue_image =  cv2.addWeighted(lower_red_hue_range, 1.0, upper_red_hue_range, 1.0, 0.0)
        return red_hue_image

    def green_range(self):
        green_hue_image = cv2.inRange(self.image, (50, 100, 50), (80, 255, 255))
        return green_hue_image

    def blue_range(self):
        blue_hue_image = cv2.inRange(self.image, (80, 50, 50), (130, 255, 255))
        return blue_hue_image

    def yellow_range(self):
        yellow_hue_image = cv2.inRange(self.image, (20, 100, 100), (30, 255, 255))
        return yellow_hue_image

    def all_colors(self):
        red_img = self.red_range()
        green_img = self.green_range()
        blue_img = self.blue_range()
        yellow_img = self.yellow_range()
        green_red_img = cv2.addWeighted(red_img, 1.0, green_img, 1.0, 0.0)
        green_red_blue_img = cv2.addWeighted(green_red_img, 1.0, blue_img, 1.0, 0.0)
        return cv2.addWeighted(green_red_blue_img, 1.0, yellow_img, 1.0, 0.0)
