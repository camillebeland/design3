import cv2


class RedFilter:
    @staticmethod
    def range(image):
        lower_red_hue_range = cv2.inRange(image, (0, 100, 100), (10, 255, 255))
        upper_red_hue_range = cv2.inRange(image, (160, 100, 100), (179, 255, 255))
        red_hue_image = cv2.addWeighted(lower_red_hue_range, 1.0, upper_red_hue_range, 1.0, 0.0)
        return red_hue_image


class GreenFilter:
    @staticmethod
    def range(image):
        green_hue_image = cv2.inRange(image, (50, 100, 50), (80, 255, 255))
        return green_hue_image


class BlueFilter:
    @staticmethod
    def range(image):
        blue_hue_image = cv2.inRange(image, (80, 50, 50), (130, 255, 255))
        return blue_hue_image


class YellowFilter:
    @staticmethod
    def range(image):
        yellow_hue_image = cv2.inRange(image, (20, 100, 100), (30, 255, 255))
        return yellow_hue_image


class AllColorFilter:
    @staticmethod
    def range(image):
        red_img = RedFilter.range(image)
        green_img = GreenFilter.range(image)
        blue_img = BlueFilter.range(image)
        yellow_img = YellowFilter.range(image)
        green_red_img = cv2.addWeighted(red_img, 1.0, green_img, 1.0, 0.0)
        green_red_blue_img = cv2.addWeighted(green_red_img, 1.0, blue_img, 1.0, 0.0)
        return cv2.addWeighted(green_red_blue_img, 1.0, yellow_img, 1.0, 0.0)
