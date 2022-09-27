import cv2  # type: ignore
from cvzone.PoseModule import PoseDetector  # type: ignore
from cvzone.SelfiSegmentationModule import SelfiSegmentation  # type: ignore

# Initialize the SelfiSegmentationModule
segmentor = SelfiSegmentation()


def whiteness_offset(img) -> float:
    """Uses the amount of white vs other noise in the image to decide a threshold for background removal

    Args:
        img (np.ndarray): The image to calculate the threshold for

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


cap = cv2.VideoCapture(0)
detector = PoseDetector()
while True:
    success, img = cap.read()
    threshold = whiteness_offset(img)
    bg_image = cv2.GaussianBlur(img, (55, 55), 0)
    clean_img = segmentor.removeBG(img, imgBg=bg_image, threshold=threshold)
    img = detector.findPose(clean_img)
    # bounding box (red box)
    lmList, bboxInfo = detector.findPosition(img, bboxWithHands=True)
    if bboxInfo:
        center = bboxInfo["center"]
        cv2.circle(img, center, 5, (255, 0, 255), cv2.FILLED)

    cv2.imshow("Image", img)
    if cv2.waitKey(1) & 0xFF == ord("q"):
        break
cap.release()
cv2.destroyAllWindows()
