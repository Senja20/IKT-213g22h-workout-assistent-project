import cv2  # type: ignore
import mediapipe as mp  # type: ignore
import numpy as np
from StateMachine.RepsStateMachine import Curl

from functions.calculate_angle_between_points import calculate_angle_between_points
from Detector.Detector import Detector

# Gives us all the drawing utilities. Going to be used to visualize the poses
mp_drawing = mp.solutions.drawing_utils

# Importing the pose estimation models
mp_pose = mp.solutions.pose

if __name__ == "__main__":
    stateMachine = Curl()
    # instance of the detector class
    detector = Detector()

    # counter for reps
    counter = 0
    # determine we are now on the up or down of the curl exercise
    stage = None

    # Video Feed
    # setting up the video capture device. The number represents the camera (can change from device to device)
    cap = cv2.VideoCapture(0)

    # Accesses a pose detection model with detection and tracking confidence of 50%
    with mp_pose.Pose(
        min_detection_confidence=0.5, min_tracking_confidence=0.5
    ) as my_pose:

        while cap.isOpened():
            # Stores what ever we get from the capture (ret is return variable (nothing here) and frame is the image)
            ret, my_frame = cap.read()

            my_image, my_results = detector.make_detections(my_frame)

            # Extract landmarks
            try:
                my_landmarks = my_results.pose_landmarks.landmark

                # Get the coordinates that we are interested in
                shoulder = [
                    my_landmarks[mp_pose.PoseLandmark.LEFT_SHOULDER.value].x,
                    my_landmarks[mp_pose.PoseLandmark.LEFT_SHOULDER.value].y,
                ]
                elbow = [
                    my_landmarks[mp_pose.PoseLandmark.LEFT_ELBOW.value].x,
                    my_landmarks[mp_pose.PoseLandmark.LEFT_ELBOW.value].y,
                ]
                wrist = [
                    my_landmarks[mp_pose.PoseLandmark.LEFT_WRIST.value].x,
                    my_landmarks[mp_pose.PoseLandmark.LEFT_WRIST.value].y,
                ]

                # Calculate angle between them
                my_angle = calculate_angle_between_points(shoulder, elbow, wrist)

                # Write the angle on the picture near the elbow itself
                cv2.putText(
                    my_image,
                    str(my_angle),
                    tuple(np.multiply(elbow, [640, 480]).astype(int)),
                    cv2.FONT_HERSHEY_SIMPLEX,
                    0.5,
                    (255, 255, 255),
                    2,
                    cv2.LINE_AA,
                )


                # Curl counter logic
                if my_angle > 160 and stateMachine.current_state.value == "State0":
                    stage = "down"

                    stateMachine.switch1()
                    print(stateMachine.current_state)
                elif my_angle > 160 and stateMachine.current_state.value == "ReturnState3":
                    stateMachine.to_initial()
                    counter += 1
                    print(stateMachine.current_state.value)

                if 160 > my_angle > 100 and stateMachine.current_state.value == "State1":
                    stateMachine.switch2()
                    print(stateMachine.current_state.value)
                if 160 > my_angle > 100 and stateMachine.current_state.value == "ReturnState2":
                    stateMachine.switch5()
                    print(stateMachine.current_state.value)

                if 100 > my_angle > 60 and stateMachine.current_state.value == "State2":
                    stateMachine.switch3()
                    print(stateMachine.current_state.value)
                elif 100 > my_angle > 60 and stateMachine.current_state.value == "ReturnState1":
                    stateMachine.switch4()
                    print(stateMachine.current_state.value)

                if my_angle < 40 and stage == "down" and stateMachine.current_state.value == "State3":
                    stage = "up"

                    stateMachine.start_return_to_init_state()
                    print(stateMachine.current_state.value)




            except:
                pass

            # Visualize the curl counter in a box
            # The blue box itself
            cv2.rectangle(my_image, (0, 0), (255, 73), (245, 117, 16), -1)

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
                str(counter),
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
                str(stage),
                (60, 60),
                cv2.FONT_HERSHEY_SIMPLEX,
                2,
                (255, 255, 255),
                1,
                cv2.LINE_AA,
            )
            lmList = detector.get_interest_points(frame = my_image, results=my_results)

            detector.mask_point(frame=my_image, lmList=lmList, pointID=13)

            # Draws the pose landmarks and the connections between them to the image
            detector.draw_pose_pose_landmark(frame=my_image, results=my_results)

            # Shows the image with the landmarks on them (after the processing)
            cv2.imshow("Mediapipe Feed", my_image)
            # Breaks the loop if you hit q
            if cv2.waitKey(10) & 0xFF == ord("q"):
                break

    # Releases the capture device
    cap.release()
    # Closes all windows
    cv2.destroyAllWindows()
