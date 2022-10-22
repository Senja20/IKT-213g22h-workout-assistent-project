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
