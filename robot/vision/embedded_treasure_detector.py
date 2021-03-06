import cv2


class EmbeddedTreasureDetector:
    def __init__(self):
        self.tracked_treasure_position = (0,0)
        self.consecutive_tracked_frame = 0
        self.consecutive_lost_frame = 0
        self.first_frame = True
        self.embedded_camera_fov = 63.53

    def __black_mask(self, image, mask_params):
        erode_kernel_size = mask_params['erode_kernel_size']
        erode_iterations = mask_params['erode_iterations']
        dilate_kernel_size = mask_params['dilate_kernel_size']
        dilate_iterations = mask_params['dilate_iterations']
        gaussian_blur_kernel_size = mask_params['gaussian_blur_kernel_size']
        gaussian_blur_sigma_x = mask_params['gaussian_blur_sigma_x']
        contours = (image
            .filter_gaussian_blur((gaussian_blur_kernel_size,gaussian_blur_kernel_size),gaussian_blur_sigma_x)
            .filter_by_color(hsv_range['black'])
            .erode(erode_kernel_size, erode_iterations)
            .dilate(dilate_kernel_size, dilate_iterations)
            .erode(erode_kernel_size, dilate_iterations - 2*erode_iterations)
            .find_contours())
        return contours

    def approx_polygon(self, contour):
        epsilon = 0.04 * cv2.arcLength(contour, True)
        return cv2.approxPolyDP(contour, epsilon, True)

    def find_biggest_contour(self, contours):
        biggest_contour_area = 0
        contour = 0
        for contour in contours:
            area = cv2.contourArea(contour)
            if area > biggest_contour_area:
                biggest_contour_area = area
        return contour

    def map_treasures(self, image, mask_params, treasures_params , opencv=cv2):
        contours = self.__black_mask(image, mask_params)

        black_area_contour = self.find_biggest_contour(contours)
        masked = image.mask_image_embedded((black_area_contour))
        erode_kernel_size = treasures_params['erode_kernel_size']
        erode_iterations = treasures_params['erode_iterations']
        dilate_kernel_size = treasures_params['dilate_kernel_size']
        dilate_iterations = treasures_params['dilate_iterations']
        gaussian_blur_kernel_size = treasures_params['gaussian_blur_kernel_size']
        gaussian_blur_sigma_x = treasures_params['gaussian_blur_sigma_x']
        
        contours = (masked
                    .filter_gaussian_blur((gaussian_blur_kernel_size,gaussian_blur_kernel_size),gaussian_blur_sigma_x)
                    .filter_by_color(hsv_range['yellow'])
                    .erode(erode_kernel_size, erode_iterations)
                    .dilate(dilate_kernel_size, dilate_iterations)
                    .find_contours())
        x_positions = []
        
        for contour in contours:
            approx = self.approx_polygon(contour)
            x, y, width, height = opencv.boundingRect(approx)
            x_positions.append(x)
        
        x_to_deg = self.embedded_camera_fov/1600
        angles = list(map(lambda x : x*x_to_deg , x_positions))
        return angles

    def track_treasure(self, image, parameters , opencv=cv2):
        resized = image.resize(800)
        erode_kernel_size = parameters['erode_kernel_size']
        erode_iterations = parameters['erode_iterations']
        dilate_kernel_size = parameters['dilate_kernel_size']
        dilate_iterations = parameters['dilate_iterations']
        gaussian_blur_kernel_size = parameters['gaussian_blur_kernel_size']
        gaussian_blur_sigma_x = parameters['gaussian_blur_sigma_x']
        min_area = parameters['min_area']
        max_area = parameters['max_area']
        max_delta_position = parameters['max_delta_position']

        contours = (resized
                    .filter_gaussian_blur((gaussian_blur_kernel_size,gaussian_blur_kernel_size),gaussian_blur_sigma_x)
                    .filter_by_color(hsv_range['yellow'])
                    .erode(erode_kernel_size, erode_iterations)
                    .dilate(dilate_kernel_size, dilate_iterations)
                    .find_contours())
        if len(contours) == 0:
            self.consecutive_lost_frame += 1
            if self.__treasure_is_lost():
                self.tracked_treasure_position = 0, 0
                self.consecutive_tracked_frame = 0
                self.first_frame = True
            return False
            
        def approx_polygon(contour):
            epsilon = 0.04*opencv.arcLength(contour, True)
            return opencv.approxPolyDP(contour, epsilon, True)
        
        center_contour_y = 0
        center_contour_x = resized.get_width()
        for contour in contours:
            approx = approx_polygon(contour)
            x, y, width, height = opencv.boundingRect(approx)
            area = opencv.contourArea(contour)
            if min_area < area <  max_area:
                if (abs(self.tracked_treasure_position[0] - x)**2 + abs(self.tracked_treasure_position[1] - y)**2)**0.5 \
                        < max_delta_position or self.first_frame is True:
                    if abs((x+width/2) - resized.get_width()/2) < center_contour_x:
                        center_contour_y = y +height/2
                        center_contour_x = x+width/2
                
        if self.first_frame is True:
            self.consecutive_tracked_frame +=1
            self.consecutive_lost_frame = 0
            self.tracked_treasure_position = (center_contour_x, center_contour_y)
            self.first_frame = False
            return True
        elif center_contour_y != 0:
            self.consecutive_tracked_frame += 1
            self.consecutive_lost_frame = 0
            self.tracked_treasure_position = (center_contour_x, center_contour_y)
            return True
        else:
            self.consecutive_lost_frame += 1
            if self.__treasure_is_lost():
                self.tracked_treasure_position = (0,0)
                self.consecutive_tracked_frame = 0
                self.first_frame = True
            return False
    
    def get_tracked_treasure_position(self):
        if self.consecutive_tracked_frame > 15:
            return self.tracked_treasure_position[0]*2, self.tracked_treasure_position[1]*2
        else:
            return 0, 0

    def __treasure_is_lost(self):
        return self.consecutive_lost_frame >= 15
        

hsv_range = {
    'yellow': ((15,100,75), (35,255,255)),
    'black':((0,0,0),(180,255,85))
}
