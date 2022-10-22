import cv2  # type: ignore
import mediapipe as mp  # type: ignore


class Detector:
    def __init__(
        self,
        mode=False,
        upBody=False,
        smoothBody=False,
        smooth=True,
        detectionCon=0.5,
        trackCon=0.5,
    ):

        self.mode = mode
        self.upBody = upBody
        self.smoothBody = smoothBody
        self.detectionCon = detectionCon
        self.trackCon = trackCon
        self.smooth = smooth

        self.results = None

        # Gives us all the drawing utilities. Going to be used to visualize the poses
        self.mp_drawing = mp.solutions.drawing_utils
        # Importing the pose estimation models
        self.mp_pose = mp.solutions.pose
        self.pose = self.mp_pose.Pose(
            static_image_mode=self.mode,
            enable_segmentation=self.upBody,
            smooth_segmentation=self.smoothBody,
            smooth_landmarks=self.smooth,
            min_detection_confidence=self.detectionCon,
            min_tracking_confidence=self.trackCon,
        )

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

    def get_interest_points(self, frame, results):
        lmList = []
        if results.pose_landmarks:
            for id, lm in enumerate(results.pose_landmarks.landmark):
                h, w, c = frame.shape
                cx, cy = int(lm.x * w), int(lm.y * h)
                lmList.append([id, cx, cy])
        return lmList

    def draw_pose_pose_landmark(self, frame, results):
        self.mp_drawing.draw_landmarks(
            frame,
            results.pose_landmarks,
            self.mp_pose.POSE_CONNECTIONS,
            # changing color and thickness of the circle drawing
            self.mp_drawing.DrawingSpec(
                color=(245, 117, 66), thickness=2, circle_radius=2
            ),
            # changing color and thicknes of the connections drawing
            self.mp_drawing.DrawingSpec(
                color=(245, 66, 230), thickness=2, circle_radius=2
            ),
        )

    def mask_point(self, frame, pointID, lmList):
        if len(lmList) != 0:
            cv2.circle(
                frame, (lmList[pointID][1], lmList[pointID][2]), 40, (255, 0, 0), 4
            )
