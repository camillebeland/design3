import cv2

class Images_Provider:
    def __init__ (self):
        self.current_image = cv2.imread('image.jpg',0)