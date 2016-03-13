# USAGE
# python detect_shapes.py --image shapes_and_colors.png

# import the necessary packages
from pyimagesearch.shapedetector import ShapeDetector
import argparse
import imutils
import cv2

yellowl = (15,80,70)
yellowu = (35,255,255)


# construct the argument parse and parse the arguments
ap = argparse.ArgumentParser()
ap.add_argument("-i", "--image", required=True,
	help="path to the input image")
args = vars(ap.parse_args())

# load the image and resize it to a smaller factor so that
# the shapes can be approximated better
image = cv2.imread(args["image"])
resized = imutils.resize(image, width=960)
ratio = 1#image.shape[0] / float(resized.shape[0])

blurred = cv2.blur(resized, (13, 13))

hsv = cv2.cvtColor(blurred, cv2.COLOR_BGR2HSV)

yellow = cv2.inRange(hsv, yellowl, yellowu)
#yellow = cv2.erode(yellow, None, iterations=1)
#yellow = cv2.dilate(yellow, None, iterations=1)
#yellow = cv2.threshold(yellow, 90, 255, cv2.THRESH_BINARY)[1]

# find contours in the thresholded image and initialize the
# shape detector
cnts = cv2.findContours(yellow.copy(), cv2.RETR_EXTERNAL,
	cv2.CHAIN_APPROX_SIMPLE)
cnts = cnt[0] if imutils.is_cv2() else cnts[1]



sd = ShapeDetector()

for c in cnts:
	# compute the center of the contour, then detect the name of the
	# shape using only the contour
	shape = sd.detect(c)
	minY = 5000
	maxY = -1
	minX = 5000
	maxX = -1
	
	for i in c:
		#print("x {} y {}".format(i[0][0], i[0][1]))
		if i[0][0] < minX:
			minX = i[0][0]
		if i[0][1] < minY:
			minY = i[0][1]
		if i[0][0] > maxX:
			maxX = i[0][0]
		if i[0][1] > maxY:
			maxY = i[0][1]

	if abs(maxX - minX) > 30:
		continue
	if abs(maxY - minY) > 30:
		continue
	area = cv2.contourArea(c)
	if (area<50):
		continue
	if (area>175):
		continue

	M = cv2.moments(c)
	if (M["m00"] == 0):
		continue
	cX = int((M["m10"] / M["m00"]) * ratio)
	cY = int((M["m01"] / M["m00"]) * ratio)

	
	cv2.drawContours(resized, [c], -1, (11, 222, 255),1)
	cv2.putText(resized, "Treasure", (cX, cY), cv2.FONT_HERSHEY_SIMPLEX,
		0.5, (255, 255, 255), 2)
		
	
	# show the output image
cv2.imshow("Image", resized)
cv2.waitKey(0)
	
