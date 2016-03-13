# USAGE
# python detect_shapes.py --image shapes_and_colors.png

# import the necessary packages
from pyimagesearch.shapedetector import ShapeDetector
import argparse
import imutils
import cv2

redl = (160,100,100)
redu = (179,255,255)
yellowl = (20,100,100)
yellowu = (30,255,255)
greenl =  (50,100,50)
greenu = (80,255,255)
bluel = (80,50,50)
blueu = (130,255,255)

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

blurred = cv2.GaussianBlur(resized, (15, 15), 0)
hsv = cv2.cvtColor(blurred, cv2.COLOR_BGR2HSV)
# convert the resized image to grayscale, blur it slightly,
# and threshold it
blue = cv2.inRange(hsv, bluel, blueu)
blue = cv2.erode(blue, None, iterations=2)
blue = cv2.dilate(blue, None, iterations=2)
blue = cv2.threshold(blue, 100, 255, cv2.THRESH_BINARY)[1]

# find contours in the thresholded image and initialize the
# shape detector
cnts1 = cv2.findContours(blue.copy(), cv2.RETR_EXTERNAL,
	cv2.CHAIN_APPROX_SIMPLE)

cnts1 = cnt1[0] if imutils.is_cv2() else cnts1[1]

yellow = cv2.inRange(hsv, yellowl, yellowu)
yellow = cv2.erode(yellow, None, iterations=2)
yellow = cv2.dilate(yellow, None, iterations=2)
yellow = cv2.threshold(yellow, 100, 255, cv2.THRESH_BINARY)[1]

# find contours in the thresholded image and initialize the
# shape detector
cnts2 = cv2.findContours(yellow.copy(), cv2.RETR_EXTERNAL,
	cv2.CHAIN_APPROX_SIMPLE)
cnts2 = cnt2[0] if imutils.is_cv2() else cnts2[1]

red = cv2.inRange(hsv, redl, redu)
red = cv2.erode(red, None, iterations=2)
red = cv2.dilate(red, None, iterations=2)
red = cv2.threshold(red, 100, 255, cv2.THRESH_BINARY)[1]

# find contours in the thresholded image and initialize the
# shape detector
cnts3 = cv2.findContours(red.copy(), cv2.RETR_EXTERNAL,
	cv2.CHAIN_APPROX_SIMPLE)
cnts3 = cnt3[0] if imutils.is_cv2() else cnts3[1]

green = cv2.inRange(hsv, greenl, greenu)
green = cv2.erode(green, None, iterations=2)
green = cv2.dilate(green, None, iterations=2)
green = cv2.threshold(green, 100, 255, cv2.THRESH_BINARY)[1]

# find contours in the thresholded image and initialize the
# shape detector
cnts4 = cv2.findContours(green.copy(), cv2.RETR_EXTERNAL,
	cv2.CHAIN_APPROX_SIMPLE)
cnts4 = cnts4[0] if imutils.is_cv2() else cnts4[1]

contour_list = (cnts1, cnts2, cnts3, cnts4)

sd = ShapeDetector()

color = ("blue", "yellow", "red", "green")
count = 0
for q in contour_list:
	# loop over the contours
	current_color = color[count]
	for c in q:
		# compute the center of the contour, then detect the name of the
		# shape using only the contour
		shape = sd.detect(c)
		minY = 5000
		maxY = -1
		minX = 5000
		maxX = -1
		epsilon = 0.02*cv2.arcLength(c,True)
		approx = cv2.approxPolyDP(c,epsilon,True)
		if (not cv2.isContourConvex(approx)):
			continue
		
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
		
		if abs(maxX - minX) > 75:
			continue
		if abs(maxY - minY) > 75:
			continue
		
		if abs(maxX - minX) < 20:
			continue
		if abs(maxY - minY) < 20:
			continue
			
		#print(abs(maxY - minY))
		#print(abs(maxX - minX))

		# multiply the contour (x, y)-coordinates by the resize ratio,
		# then draw the contours and the name of the shape on the image
		M = cv2.moments(c)
		cX = int((M["m10"] / M["m00"]) * ratio)
		cY = int((M["m01"] / M["m00"]) * ratio)
		
		cv2.drawContours(resized, [c], -1, (0, 255, 0), 2)
		cv2.putText(resized, shape+" "+current_color, (cX, cY), cv2.FONT_HERSHEY_SIMPLEX,
			0.5, (255, 255, 255), 2)
			
	count = count +1
	
	# show the output image
cv2.imshow("Image", resized)
	#cv2.imshow("Image", image)
cv2.waitKey(0)
	
