import cv2

def find_shape_height_and_lenght(contour):
    leftest_vertex = min([vertex[0][0] for vertex in contour])
    lowest_vertex = min([vertex[0][1] for vertex in contour])
    rightest_vertex = max([vertex[0][0] for vertex in contour])
    upper_vertex = max([vertex[0][1] for vertex in contour])

    return leftest_vertex, lowest_vertex, rightest_vertex, upper_vertex


def find_coordinates(image, contour):
    worldmap_object = {}
    moment = cv2.moments(contour)
    center_x = int((moment["m10"] / moment["m00"]))
    centrer_y = int((moment["m01"] / moment["m00"]))
    worldmap_object['x'] = center_x
    worldmap_object['y'] = image.get_height() - centrer_y
    return worldmap_object