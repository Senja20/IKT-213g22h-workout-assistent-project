import cv2 # type: ignore
import mediapipe as mp # type: ignore
import numpy as np

# Gives us all the drawing utilities. Going to be used to visualize the poses
mp_drawing = mp.solutions.drawing_utils

# Importing the pose estimation models
mp_pose = mp.solutions.pose


def make_detections(pose, frame):
    # Recolor the frame (opencv gives the image in BGR format. while mediapipe uses images in RGB format)
    image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    # saves memory when we pass it to the pose estimation model?
    image.flags.writeable = False

    # Make the detection (stores the detection)
    results = pose.process(image)

    # Recolor the image back to BGR
    image.flags.writeable = True
    image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)

    return image, results


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


if __name__ == "__main__":
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

            my_image, my_results = make_detections(my_pose, my_frame)

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
                if my_angle > 160:
                    stage = "down"

                if my_angle < 30 and stage == "down":
                    stage = "up"
                    counter += 1
                    print(counter)

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

            # Draws the pose landmarks and the connections between them to the image
            mp_drawing.draw_landmarks(
                my_image,
                my_results.pose_landmarks,
                mp_pose.POSE_CONNECTIONS,
                # changing color and thickness of the circle drawing
                mp_drawing.DrawingSpec(
                    color=(245, 117, 66), thickness=2, circle_radius=2
                ),
                # changing color and thicknes of the connections drawing
                mp_drawing.DrawingSpec(
                    color=(245, 66, 230), thickness=2, circle_radius=2
                ),
            )

            # Shows the image with the landmarks on them (after the processing)
            cv2.imshow("Mediapipe Feed", my_image)

            # Breaks the loop if you hit q
            if cv2.waitKey(10) & 0xFF == ord("q"):
                break

    # Releases the capture device
    cap.release()
    # Closes all windows
    cv2.destroyAllWindows()
