import numpy as np

def cos(angle):
    return np.cos(angle/180 * np.pi)

def sin(angle):
    return np.sin(angle/180 * np.pi)

def rotation_matrix(theta):
    return np.array([[cos(theta), -1*sin(theta)], [sin(theta), cos(theta)]])

def rotate_vector(theta, position):
    vector = np.array(position.to_tuple())
    return np.dot(rotation_matrix(theta), vector)


