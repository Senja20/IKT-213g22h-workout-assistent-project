"""
Proof of concept for a workout assistant, utilizing Mediapipe, OpenCV, and
our own custom code (some based on CVZone).
Detects repetitions for pushups.
"""
import time
from datetime import datetime

import cv2  # type: ignore
import mediapipe as mp  # type: ignore

from datebase.add_record import add_record  # type: ignore
from Detector.Detector import Detector  # type: ignore
from ROI.ROI import ROI  # type: ignore
from SelfieSegmentation.selfie_segmentation import SelfieSegmentation  # type: ignore
from StateMachine.RepsStateMachine import Exercise  # type: ignore
from Utility.fps import FPS  # type: ignore
from Utility.utility import define_body_part, whiteness_offset  # type: ignore

# Gives us all the drawing utilities. Going to be used to visualize the poses
mp_drawing = mp.solutions.drawing_utils

# Importing the pose estimation models
mp_pose = mp.solutions.pose


if __name__ == "__main__":

    start_time = 0.0
    duration_time = 60.0
    remaining_time = 60.0

    push_up = Exercise()
    # instance of the detector class
    detector = Detector(upBody=True, smoothBody=True)
    # Initialize the SelfieSegmentationModule
    segmenter = SelfieSegmentation()

    # region of interest
    roi = ROI()

    # Initialize the FPS reader for displaying on the final image
    fps_injector = FPS()

    # Video Feed setting up the video capture device. The number represents the
    # camera (can change from device to device)
    cap = cv2.VideoCapture(0)

    # Accesses a pose detection model with detection and tracking confidence of
    # 50%
    with mp_pose.Pose(
        min_detection_confidence=0.5, min_tracking_confidence=0.5
    ) as my_pose:
        start_time = time.time()
        while cap.isOpened() and remaining_time > 0.5:
            # Stores what ever we get from the capture (ret is return variable
            # (nothing here) and frame is the image)
            ret, my_frame = cap.read()

            if roi.roi_detected:
                my_frame = roi.add_region_of_interest(my_frame)

            my_image, my_results = detector.make_detections(my_frame)

            # Extract landmarks
            try:
                my_landmarks = my_results.pose_landmarks.landmark

                if push_up.reps and not roi.roi_detected:
                    roi.detect_roi(my_image, my_landmarks)

                VISIBILITY_THRESHOLD = 0.6

                # Get the coordinates that we are interested in
                shoulder_left = define_body_part(
                    mp_pose.PoseLandmark.LEFT_SHOULDER.value,
                    my_landmarks,
                    VISIBILITY_THRESHOLD,
                )
                elbow_left = define_body_part(
                    mp_pose.PoseLandmark.LEFT_ELBOW.value,
                    my_landmarks,
                    VISIBILITY_THRESHOLD,
                )
                wrist_left = define_body_part(
                    mp_pose.PoseLandmark.LEFT_WRIST.value,
                    my_landmarks,
                    VISIBILITY_THRESHOLD,
                )
                hip_left = define_body_part(
                    mp_pose.PoseLandmark.LEFT_HIP.value,
                    my_landmarks,
                    VISIBILITY_THRESHOLD,
                )
                knee_left = define_body_part(
                    mp_pose.PoseLandmark.LEFT_KNEE.value,
                    my_landmarks,
                    VISIBILITY_THRESHOLD,
                )

                shoulder_right = define_body_part(
                    mp_pose.PoseLandmark.RIGHT_SHOULDER.value,
                    my_landmarks,
                    VISIBILITY_THRESHOLD,
                )
                elbow_right = define_body_part(
                    mp_pose.PoseLandmark.RIGHT_ELBOW.value,
                    my_landmarks,
                    VISIBILITY_THRESHOLD,
                )
                wrist_right = define_body_part(
                    mp_pose.PoseLandmark.RIGHT_WRIST.value,
                    my_landmarks,
                    VISIBILITY_THRESHOLD,
                )
                hip_right = define_body_part(
                    mp_pose.PoseLandmark.RIGHT_HIP.value,
                    my_landmarks,
                    VISIBILITY_THRESHOLD,
                )
                knee_right = define_body_part(
                    mp_pose.PoseLandmark.RIGHT_KNEE.value,
                    my_landmarks,
                    VISIBILITY_THRESHOLD,
                )

                push_up.update_state(
                    shoulder_left=shoulder_left,
                    elbow_left=elbow_left,
                    wrist_left=wrist_left,
                    shoulder_right=shoulder_right,
                    elbow_right=elbow_right,
                    wrist_right=wrist_right,
                    hip_left=hip_left,
                    hip_right=hip_right,
                    knee_left=knee_left,
                    knee_right=knee_right,
                )
                remaining_time = duration_time - (time.time() - start_time)
                cv2.putText(
                    my_image,
                    ("{:.2f}".format(round(remaining_time, 2))),
                    (150, 120),
                    cv2.FONT_HERSHEY_SIMPLEX,
                    2,
                    (0, 0, 255),
                    1,
                    cv2.LINE_AA,
                )
            except AttributeError:
                # If there is no pose detected (NoneType Attribute error), pass
                pass

            # Visualize the curl counter in a box
            # The blue box itself
            cv2.rectangle(my_image, (0, 0), (255, 73), (245, 117, 16), -1)
            # Box for visibility / straightness
            cv2.rectangle(my_image, (0, 73), (100, 73 * 2), (200, 200, 200), -1)
            # Box for posture abort
            if push_up.posture_abort:
                cv2.rectangle(my_image, (0, 73 * 2), (255, 73 * 3), (0, 0, 200), -1)
            # Box for bad posture
            if push_up.bad_posture:
                cv2.rectangle(my_image, (0, 73 * 3), (255, 73 * 4), (100, 100, 200), -1)

            # The reps text in the box
            cv2.putText(
                my_image,
                "REPS",
                (15, 12),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.5,
                (0, 0, 0),
                1,
                cv2.LINE_AA,
            )

            cv2.putText(
                my_image,
                str(push_up.reps),
                (10, 60),
                cv2.FONT_HERSHEY_SIMPLEX,
                2,
                (255, 255, 255),
                1,
                cv2.LINE_AA,
            )

            # The stage text in the box
            cv2.putText(
                my_image,
                "STAGE",
                (65, 12),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.5,
                (0, 0, 0),
                1,
                cv2.LINE_AA,
            )

            cv2.putText(
                my_image,
                str(push_up.push_up.current_state.value),
                (60, 60),
                cv2.FONT_HERSHEY_SIMPLEX,
                1,
                (255, 255, 255),
                1,
                cv2.LINE_AA,
            )

            # Visibility helpers
            cv2.putText(
                my_image,
                "L",
                (10, 120),
                cv2.FONT_HERSHEY_SIMPLEX,
                1,
                (200, 0, 0) if push_up.left_hand_visibility else (0, 0, 200),
                1,
                cv2.LINE_AA,
            )
            cv2.putText(
                my_image,
                "R",
                (30, 120),
                cv2.FONT_HERSHEY_SIMPLEX,
                1,
                (200, 0, 0) if push_up.right_hand_visibility else (0, 0, 200),
                1,
                cv2.LINE_AA,
            )
            cv2.putText(
                my_image,
                "B",
                (50, 120),
                cv2.FONT_HERSHEY_SIMPLEX,
                1,
                (200, 0, 0) if push_up.back.is_straight else (0, 0, 200),
                1,
                cv2.LINE_AA,
            )
            cv2.putText(
                my_image,
                "Posture Abort!" if push_up.posture_abort else "",
                (10, 200),
                cv2.FONT_HERSHEY_SIMPLEX,
                1,
                (255, 255, 255),
                1,
                cv2.LINE_AA,
            )
            cv2.putText(
                my_image,
                "Bad posture" if push_up.bad_posture else "",
                (10, 250),
                cv2.FONT_HERSHEY_SIMPLEX,
                1,
                (255, 255, 255),
                1,
                cv2.LINE_AA,
            )

            # Get landmarks list
            lmList = detector.get_interest_points(frame=my_image, results=my_results)

            # Draw circles on angle keypoints
            detector.mask_point(frame=my_image, lmList=lmList, pointID=13)
            detector.mask_point(frame=my_image, lmList=lmList, pointID=14)
            detector.mask_point(frame=my_image, lmList=lmList, pointID=23)
            detector.mask_point(frame=my_image, lmList=lmList, pointID=24)

            # Draws the pose landmarks and the connections between them to the image
            detector.draw_pose_pose_landmark(frame=my_image, results=my_results)

            # Inject the FPS onto the frame
            fps_injector.update(my_image, (20, 300))

            # Shows the image with the landmarks on them (after the processing)
            cv2.imshow("Mediapipe Feed", my_image)
            # Breaks the loop if you hit q
            if cv2.waitKey(10) & 0xFF == ord("q"):
                break

    record = [(datetime.now(), push_up.reps)]
    add_record(record)
    # Releases the capture device
    cap.release()
    # Closes all windows
    cv2.destroyAllWindows()
