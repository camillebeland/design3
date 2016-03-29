def find_shape_height_and_lenght(contour):
    leftest_vertex = min([vertex[0][0] for vertex in contour])
    lowest_vertex = min([vertex[0][1] for vertex in contour])
    rightest_vertex = max([vertex[0][0] for vertex in contour])
    upper_vertex = max([vertex[0][1] for vertex in contour])

    return leftest_vertex, lowest_vertex, rightest_vertex, upper_vertex
