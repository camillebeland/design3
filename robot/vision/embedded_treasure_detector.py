import cv2
track_treasure_params = {
	'gaussian_blur_kernel_size' : 15,
	'gaussian_blur_sigma_x' : 0,
	'dilate_kernel_size' : 0,
	'dilate_iterations' : 5,
	'erode_kernel_size' : 0,
	'erode_iterations' : 5,
	'min_area': 100,
	'max_area': 50000
}
mask_params = {
	'gaussian_blur_kernel_size' : 15,
	'gaussian_blur_sigma_x' : 0,
	'dilate_kernel_size' : 0,
	'dilate_iterations' : 60,
	'erode_kernel_size' : 0,
	'erode_iterations' : 5
}

map_treasures_params = {
	'gaussian_blur_kernel_size' : 7,
	'gaussian_blur_sigma_x' : 0,
	'dilate_kernel_size' : 0,
	'dilate_iterations' : 2,
	'erode_kernel_size' : 0,
	'erode_iterations' : 2,
}



max_delta_position = 250

# ************ EMBEDDED CAMERA FOV IS 63.53 deg *****************

class EmbeddedTreasureDetector:

	def __init__(self, embedded_camera_controller):
		self.tracked_treasure_position = (0,0)
		self.consecutive_tracked_frame = 0
		self.consecutive_lost_frame = 0
		self.embedded_camera_controller = embedded_camera_controller
		
	def map_treasures(self, mask_params = mask_params, treasures_params = map_treasures_params, opencv=cv2):
		
		
		#camera must be in correct orientation (straight)
		#DO IT HERE IF YOU WANT TO :D
		
		image = self.embedded_camera_controller.get_image()
		#black mask
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
			.erode(erode_kernel_size, dilate_iterations - erode_iterations)
			.find_contours())

		def find_biggest_contour(cnts):
			biggest_contour_area = 0
			biggest_contour = 0
			contour = 0
			for contour in cnts:
				area = cv2.contourArea(contour)
				if area > biggest_contour_area:
					biggest_contour_area = area
					biggest_contour = contour
			return contour

		black_area_contour = find_biggest_contour(contours)
		masked = image.mask_image_embedded((black_area_contour))
		#find all contours that matches a treasure within the masked image
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
		def approx_polygon(contour, opencv=cv2):
			epsilon = 0.04*cv2.arcLength(contour, True)
			return opencv.approxPolyDP(contour, epsilon, True)
		
		x_positions = []
		
		for contour in contours:
			approx = approx_polygon(contour)
			x, y, width, height = cv2.boundingRect(approx)
			x_positions.append(x)
				
		#return x positions of all treasures relative to FOV
		return x_positions
		
		
		
	def track_treasure(self, parameters = track_treasure_params, opencv=cv2):
		image = embedded_camera_controller.get_image()
		erode_kernel_size = parameters['erode_kernel_size']
		erode_iterations = parameters['erode_iterations']
		dilate_kernel_size = parameters['dilate_kernel_size']
		dilate_iterations = parameters['dilate_iterations']
		gaussian_blur_kernel_size = parameters['gaussian_blur_kernel_size']
		gaussian_blur_sigma_x = parameters['gaussian_blur_sigma_x']
		min_area = parameters['min_area']
		max_area = parameters['max_area']

		contours = (image
					.filter_gaussian_blur((gaussian_blur_kernel_size,gaussian_blur_kernel_size),gaussian_blur_sigma_x)
					.filter_by_color(hsv_range['yellow'])
					.erode(erode_kernel_size, erode_iterations)
					.dilate(dilate_kernel_size, dilate_iterations)
					.find_contours())
		
		def approx_polygon(contour):
			epsilon = 0.04*cv2.arcLength(contour, True)
			return opencv.approxPolyDP(contour, epsilon, True)
		
		highest_contour = 0
		highest_contour_y = image.get_height()
		highest_contour_x = 0
		for contour in contours:
			approx = approx_polygon(contour)
			x, y, width, height = cv2.boundingRect(approx)
			area = cv2.contourArea(contour)
			if (min_area < area <  max_area and y < highest_contour_y):
				highest_contour = contour
				highest_contour_y = y +height/2
				highest_contour_x = x+width/2
		
		if (highest_contour_x != 0 and (abs(self.last_treasure_position[0] - highest_contour_x)**2 + abs(self.last_treasure_position[1] - highest_contour_y)**2)**(0.5) < max_delta_position):
			consecutive_tracked_frame = consecutive_tracked_frame+1
			consecutive_lost_frame = 0
			self.tracked_treasure_position = (highest_contour_x, highest_contour_y)
			return True
		else:
			consecutive_lost_frame = consecutive_lost_frame +1
			if (consecutive_lost_frame >= 30): #we lost the treasure :(
				self.tracked_treasure_position = (0,0)
				consecutive_tracked_frame = 0
			return False
	
	def get_tracked_treasure_position(self):
		if (self.consecutive_tracked_frame > 30):
			return tracked_treasure_position
		else:
			return (0,0)
		

hsv_range = {
	'yellow': ((15,100,75), (35,255,255)),
	'black':((0,0,0),(180,255,85))
}
