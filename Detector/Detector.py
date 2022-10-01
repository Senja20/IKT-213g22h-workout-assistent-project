import cv2
import mediapipe as mp
import time

class Detector:
    def __init__(self, mode=False,
                 upBody=False,
                 smooth=True,
                 detectionCon=0.5,
                 trackCon=0.5):
        self.mode = mode
        self.upBody = upBody
        self.detectionCon = detectionCon
        self.trackCon = trackCon
        self.smooth = smooth

        self.results = None
        self.mp_drawing = mp.solutions.drawing_utils
        self.mp_pose = mp.solutions.pose
        self.pose = self.mp_pose.Pose(static_image_mode=self.mode,
                                     enable_segmentation=self.upBody,
                                     smooth_landmarks=self.smooth,
                                     min_detection_confidence=self.detectionCon,
                                     min_tracking_confidence=self.trackCon)

    def make_detections(self, frame):
        # Recolor the frame (opencv gives the image in BGR format. while mediapipe uses images in RGB format)
        image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        # saves memory when we pass it to the pose estimation model?
        image.flags.writeable = False

        # Make the detection (stores the detection)
        self.results = self.pose.process(image)

        # Recolor the image back to BGR
        image.flags.writeable = True
        image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)

        return image, self.results

    def get_interest_points(self, img, results):
        lmList = []
        if results.pose_landmarks:
            for id, lm in enumerate(results.pose_landmarks.landmark):
                h, w, c = img.shape
                cx, cy = int(lm.x * w), int(lm.y * h)
                lmList.append([id, cx, cy])
        return lmList