import cv2

if __name__ == '__main__':
    bgr_image = cv2.imread("circlesImage.jpg")
    orig_image = bgr_image
    bgr_image = cv2.medianBlur(bgr_image, 3)
    hsv_image = cv2.cvtColor(bgr_image, cv2.COLOR_BGR2HSV)

    lower_red_hue_range = cv2.inRange(hsv_image, (0, 100, 100), (10, 255, 255))
    upper_red_hue_range = cv2.inRange(hsv_image, (160, 100, 100), (179, 255, 255))

    red_hue_image = cv2.addWeighted(lower_red_hue_range, 1.0, upper_red_hue_range, 1.0, 0.0)
    red_hue_image = cv2.GaussianBlur(red_hue_image, (9, 9), 2, 2)
    circles = cv2.HoughCircles(red_hue_image, cv2.HOUGH_GRADIENT, 1, len(red_hue_image) / 8,
                               param1=50, param2=30, minRadius=0, maxRadius=0)

    for x in circles[0,:]:
         center_point = (x[0], x[1])
         radius = x[2]
         cv2.circle(orig_image, center_point, radius, (0, 255, 0), 2)
         cv2.circle(orig_image, center_point,2,(0,0,255),3)

    cv2.imshow("Detected red circles on the input image", orig_image)
    cv2.waitKey(0)