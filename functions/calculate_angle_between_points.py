import numpy as np

def calculate_angle_between_points(pointA, pointB, pointC):
    # convert the point to numpy arrays
    pointA = np.array(pointA)  # first point
    pointB = np.array(pointB)  # mid point
    pointC = np.array(pointC)  # last point

    # calculate the angle using trigonometry and convert it to degrees
    angle_in_radians = np.arctan2(
        pointC[1] - pointB[1], pointC[0] - pointB[0]
    ) - np.arctan2(pointA[1] - pointB[1], pointA[0] - pointB[0])
    angle_in_degrees = np.abs(angle_in_radians * 180.0 / np.pi)

    if angle_in_degrees > 180.0:
        angle_in_degrees = 360 - angle_in_degrees

    return angle_in_degrees