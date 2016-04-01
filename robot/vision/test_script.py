import cv2
from embedded_treasure_detector import EmbeddedTreasureDetector as etd
import argparse
from image_wrapper import ImageWrapper as IW
# construct the argument parse and parse the arguments
ap = argparse.ArgumentParser()
ap.add_argument("-v", "--video",
    help="path to the (optional) video file")
ap.add_argument("-b", "--buffer", type=int, default=64,
    help="max buffer size")
args = vars(ap.parse_args())

if not args.get("video", False):
    camera = cv2.VideoCapture(0)
    camera.set(3,1600)
    camera.set(4,1200)
# otherwise, grab a reference to the video file
else:
    camera = cv2.VideoCapture(args["video"])

#mock class for the embedded camera controller
class controller:
    def __init__(self, camera):
        self.camera = camera
    def get_image(self):
        (grabbed, frame) = camera.read()
        return IW(frame)
        
myController = controller(camera)
myETD = etd(myController)
map = myETD.map_treasures()
print(map)