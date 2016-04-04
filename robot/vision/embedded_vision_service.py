import cv2
from image_wrapper import ImageWrapper as IW
from time import sleep

#on doit lui passer un camera_service, un camera_rotation_control et les detector

class EmbeddedVisionService:
	def __init__(self, camera_service,  camera_rotation_control, embedded_treasure_detector):
		self.camera = camera_service
		self.camera_rotation_control = camera_rotation_control
		self.embedded_treasure_detector = embedded_treasure_detector
		
	def get_treasure_map(self):
		self.camera_rotation_control.set_hor(0)
		self.camera_rotation_control.set_ver(0)
		sleep(1)
		return self.embedded_treasure_detector.map_treasures(IW(self.camera.get_frame()), mask_params, map_treasures_params)
	
	def track_treasure(self):
		image = IW(self.camera.get_frame())
		self.embedded_treasure_detector.track_treasure(image, track_treasure_params)
		
	def get_tracked_treasure_position(self):
		return self.embedded_treasure_detector.get_tracked_treasure_position()
	
		
track_treasure_params = {
	'gaussian_blur_kernel_size' : 15,
	'gaussian_blur_sigma_x' : 0,
	'dilate_kernel_size' : 0,
	'dilate_iterations' : 5,
	'erode_kernel_size' : 0,
	'erode_iterations' : 5,
	'min_area': 100,
	'max_area': 50000,
	'max_delta_position' : 250
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


