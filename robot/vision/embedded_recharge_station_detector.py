import cv2
from vision_utils.image_wrapper import ImageWrapper as Image


class EmbeddedRechargeStationDetector:
    def __init__(self):
        self.tracked_marker_position = (0,0)
        self.consecutive_tracked_frame = 0
        self.consecutive_lost_frame = 0
        self.first_frame = True

    def __find_blue_contours(self, image, mask_params):
        erode_kernel_size = mask_params['erode_kernel_size']
        erode_iterations = mask_params['erode_iterations']
        dilate_kernel_size = mask_params['dilate_kernel_size']
        dilate_iterations = mask_params['dilate_iterations']
        gaussian_blur_kernel_size = mask_params['gaussian_blur_kernel_size']
        gaussian_blur_sigma_x = mask_params['gaussian_blur_sigma_x']
        contours = (image
                    .filter_gaussian_blur((gaussian_blur_kernel_size,gaussian_blur_kernel_size),gaussian_blur_sigma_x)
                    .filter_by_color(hsv_range['blue'])
                    .erode(erode_kernel_size, erode_iterations)
                    .dilate(dilate_kernel_size, dilate_iterations)
                    .erode(erode_kernel_size, dilate_iterations - erode_iterations)
                    .find_contours())
        return contours

    def approx_polygon(self, contour):
        epsilon = 0.04 * cv2.arcLength(contour, True)
        return cv2.approxPolyDP(contour, epsilon, True)
        
    def track_marker_position(self, image, mask_params, marker_params , opencv=cv2):
        resized = image.resize(800)
        blue_contours = self.__find_blue_contours(resized, mask_params)

        if len(blue_contours) == 0:
            self.__lost()
            return False
            
        def find_biggest_contour(contours):
            biggest_contour_area = 0
            contour = 0
            for contour in contours:
                area = opencv.contourArea(contour)
                if area > biggest_contour_area:
                    biggest_contour_area = area
            return contour
        
        blue_area_contour = find_biggest_contour(blue_contours)
        masked = resized.mask_image_embedded(blue_area_contour)
        erode_kernel_size = marker_params['erode_kernel_size']
        erode_iterations = marker_params['erode_iterations']
        dilate_kernel_size = marker_params['dilate_kernel_size']
        dilate_iterations = marker_params['dilate_iterations']
        gaussian_blur_kernel_size = marker_params['gaussian_blur_kernel_size']
        gaussian_blur_sigma_x = marker_params['gaussian_blur_sigma_x']
        max_delta_position = marker_params['max_delta_position']
        
        redUp = (masked
                    .filter_gaussian_blur((gaussian_blur_kernel_size,gaussian_blur_kernel_size),gaussian_blur_sigma_x)
                    .filter_by_color(hsv_range['red_upper'])
                    .read_image())
                    
        redDown = (masked
                    .filter_gaussian_blur((gaussian_blur_kernel_size,gaussian_blur_kernel_size),gaussian_blur_sigma_x)
                    .filter_by_color(hsv_range['red_lower'])
                    .read_image())
        
        contours = (Image(redDown+redUp)
                    .erode(erode_kernel_size, erode_iterations)
                    .dilate(dilate_kernel_size, dilate_iterations)
                    .find_contours())

        if len(contours) == 0:
            self.__lost()
            return False
        
        biggest_contour = find_biggest_contour(contours)
        approx = self.approx_polygon(biggest_contour)
        x, y, width, height = opencv.boundingRect(approx)
        
        if self.first_frame is True:
            self.__tracked(x+width/2, y+height/2)
            return True
            
        elif (abs(self.tracked_marker_position[0] - (x+width/2))**2 + abs(self.tracked_marker_position[1] - (y+height/2))**2)**0.5 < max_delta_position:
            self.__tracked(x+width/2, y+height/2)
            return True
        else:
            self.consecutive_lost_frame +=1
            if self.__treasure_is_lost():
                self.__lost()
                return False

    def get_tracked_marker_position(self):
        if self.consecutive_tracked_frame > 15:
            return self.tracked_marker_position[0]*2,self.tracked_marker_position[1]*2
        else:
            return 0, 0
    
    def __tracked(self,x,y):
        self.consecutive_tracked_frame +=1
        self.consecutive_lost_frame = 0
        self.tracked_marker_position = (x, y)
        self.first_frame = False
        
    def __lost(self):
        self.consecutive_lost_frame += 1
        if self.__treasure_is_lost():
            self.tracked_treasure_position = 0, 0
            self.consecutive_tracked_frame = 0
            self.first_frame = True

    def __treasure_is_lost(self):
        return self.consecutive_lost_frame >= 15
        
hsv_range = {
    'blue': ((80,50,130), (130,255,255)),
    'red_lower': ((0, 100, 100), (10, 255, 255)),
    'red_upper': ((160,100,100), (179,255,255))
}
