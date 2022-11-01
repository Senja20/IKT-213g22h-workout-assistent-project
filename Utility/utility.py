"""
General collection of utility functions
"""
import cv2  # type: ignore


def whiteness_offset(img) -> float:
    """Uses the amount of white vs other noise in the image to decide a threshold for background removal

    Args:
        img (np.nparray): The image to calculate the threshold for

    Returns:
        float: The threshold to use for background removal
    """
    # Convert the image to grayscale
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    # Calculate the average pixel value
    avg = gray.mean()
    # Calculate the threshold
    thresh = avg / 255
    return thresh


def define_body_part(lm_id: int, landmarks: list, threshold: float = 0.5) -> tuple:
    """Defines the body part based on the landmarks.

    Args:
        id (int): The id of the body part, based on PoseLandmark enum
        landmarks (list): The landmarks from the pose detection
        threshold (float, optional): The threshold to use for the detection. Defaults to 0.5.

    Returns:
        tuple: The x and y coordinates of the body part. If the body part is not visible, an empty tuple is returned
    """
    return (
        (
            landmarks[lm_id].x,
            landmarks[lm_id].y,
        )
        if landmarks[lm_id].visibility > threshold
        else tuple()
    )


def get_available_cameras() -> list:
    """Returns a list of available cameras.

    Returns:
        list: A list of available cameras
    """
    print("Available devices:")
    index = 0
    cameras = []
    while True:
        cap = cv2.VideoCapture(index)
        if not cap.read()[0]:
            break
        cameras.append(index)
        cap.release()
        index += 1
    return cameras
