from base_station.vision import Image

class VisionService:
    def __init__(self, camera, shape_detector):
        self.__camera = camera
        self.__shape_detector = shape_detector

    def build_map(self):
        image = Image(self.__camera.get_frame())
        circles = self.__shape_detector.find_circle_color(image, 'green', default_camille_circle_params)
        for circle in circles:
            circle['shape'] = 'circle'
            circle['color'] = 'green'
        worldmap = {
            'islands': circles
        }
        return worldmap

default_camille_circle_params = {
    'median_blur_kernel_size' : 5,
    'gaussian_blur_kernel_size' : 9,
    'gaussian_blur_sigma_x' : 2,
    'hough_circle_min_distance' : 50,
    'hough_circle_param1' : 50,
    'hough_circle_param2' : 30,
    'hough_circle_min_radius' : 0,
    'hough_circle_max_radius' : 0
}
