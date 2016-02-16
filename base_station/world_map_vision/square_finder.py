import numpy as np
from base_station.world_map_vision.color_ranges import ColorFilter
import cv2


def angle_cos(p0, p1, p2):
    d1, d2 = (p0 - p1).astype('float'), (p2 - p1).astype('float')
    return abs(np.dot(d1, d2) / np.sqrt(np.dot(d1, d1) * np.dot(d2, d2)))


def find_squares(img):
    squares = []
    pentagons = []
    triangles = []
    hsv_image = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)

    color_filter = ColorFilter(hsv_image)
    filtered_image = color_filter.red_range()
    cv2.imshow("lol",filtered_image)

    gaussian_image = cv2.GaussianBlur(filtered_image, (5, 5), 0)
    for gray in cv2.split(gaussian_image):
        for thrs in range(0, 255, 26):
            if thrs == 0:
                bin = cv2.Canny(gray, 0, 50, apertureSize=5)
                bin = cv2.dilate(bin, None)
            else:
                retval, bin = cv2.threshold(gray, thrs, 255, cv2.THRESH_BINARY)
            bin, contours, hierarchy = cv2.findContours(bin, cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)
            for cnt in contours:
                cnt_len = cv2.arcLength(cnt, True)
                cnt = cv2.approxPolyDP(cnt, 0.02 * cnt_len, True)
                if len(cnt) == 3 and cv2.contourArea(cnt) > 1000 and cv2.isContourConvex(cnt):
                    triangles.append(cnt)
                if len(cnt) == 5 and cv2.contourArea(cnt) > 1000 and cv2.isContourConvex(cnt):
                    pentagons.append(cnt)
                if len(cnt) == 4 and cv2.contourArea(cnt) > 1000 and cv2.isContourConvex(cnt):
                    cnt = cnt.reshape(-1, 2)
                    max_cos = np.max([angle_cos(cnt[i], cnt[(i + 1) % 4], cnt[(i + 2) % 4]) for i in range(4)])
                    if max_cos < 0.1:
                        squares.append(cnt)
    return squares, triangles, pentagons

if __name__ == '__main__':
    img = cv2.imread("circlesImage.jpg")
    squares, triangles, pentagons = find_squares(img)
    cv2.drawContours(img, squares, -1, (0, 255, 0), 3) #green
    cv2.drawContours(img, triangles, -1, (255, 0, 0), 3) #blue
    cv2.drawContours(img, pentagons, -1, (0, 0, 255), 3) #red
    cv2.imshow('squares', img)
    ch = 0xFF & cv2.waitKey()
    cv2.destroyAllWindows()
