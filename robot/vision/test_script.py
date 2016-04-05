import cv2
from embedded_treasure_detector import EmbeddedTreasureDetector as ETD
from embedded_camera_service import EmbeddedCameraService as ECS
from embedded_vision_service import EmbeddedVisionService as EVS
from embedded_recharge_station_detector import EmbeddedRechargeStationDetector as ERSD
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

class MockCameraControl:
	def set_hor(self, x):
		pass
	def set_ver(self, y):
		pass

control = MockCameraControl()
cam = ECS(camera)
treasure_detector = ETD()
recharge_detector = ERSD()
embedded_vision = EVS(cam, control, treasure_detector, recharge_detector)
map = embedded_vision.get_treasure_map()
while True:
	
	#embedded_vision.track_treasure()
	#cv2.imshow("Frame", image)
	#print(embedded_vision.get_tracked_treasure_position())
	embedded_vision.track_marker()
	print(embedded_vision.get_recharge_station_position())
	#print(treasure_detector.consecutive_tracked_frame)
	#key = cv2.waitKey(1) & 0xFF

	#if the 'q' key is pressed, stop the loop
#if key == ord("q"):
	#break

#cleanup the vision_utils and close any open windows
camera.release()
cv2.destroyAllWindows()



