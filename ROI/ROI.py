import cv2
import numpy as np

class ROI: 
    def __init__(self, roi_detected = False):
        self.roi_detected: bool = roi_detected
        self.roi_polygon: np.array
        self.roi_image: np.array

    def detect_roi(self, image, landmarks):
        image_height, image_width = image.shape[:2]

        minimum_x = image_width
        minimum_y = image_height
        maximum_x = 0
        maximum_y = 0

        for landmark in landmarks:

            if landmark.x <= minimum_x:
                minimum_x = landmark.x

            if landmark.y <= minimum_y:
                minimum_y = landmark.y

            if landmark.x > maximum_x:
                maximum_x = landmark.x

            if landmark.y > maximum_y:
                maximum_y = landmark.y

        roi_min_x = minimum_x*image_width - image_width*0.1
        roi_max_x = maximum_x*image_width + image_width*0.1
        roi_min_y = minimum_y*image_height - image_height*0.1
        roi_max_y = maximum_y*image_height + image_height*0.1

        self.roi_detected = 'true'

        self.roi_polygon = np.array([[(roi_min_x , roi_max_y), (roi_min_x, roi_min_y),
        (roi_max_x, roi_min_y), (roi_max_x, roi_max_y)]], dtype= np.int32)

    def add_region_of_interest(self, image: np.array):
        blank = np.zeros(image.shape[0:2], dtype='uint8')

        region_of_interest = cv2.fillPoly(blank, self.roi_polygon, color=(255, 255, 255))
        mask = cv2.bitwise_or(blank, region_of_interest)
        
        self.roi_image = cv2.bitwise_and(image, image, mask = mask)
        
        return self.roi_image