"""
FPS Module
By: Computer Vision Zone
Website: https://www.computervision.zone/

Slightly modified for our project
"""

import time

import cv2  # type: ignore


class FPS:
    """
    Helps in finding Frames Per Second and display on an OpenCV Image
    """

    def __init__(self):
        self.pTime = time.time()

    def update(self, img=None, pos=(20, 50), color=(255, 0, 0), scale=3, thickness=3):
        """
        Update the frame rate
        :param img: Image to display on, can be left blank if only fps value required
        :param pos: Position on the FPS on the image
        :param color: Color of the FPS Value displayed
        :param scale: Scale of the FPS Value displayed
        :param thickness: Thickness of the FPS Value displayed
        :return:
        """
        cTime = time.time()
        try:
            fps = 1 / (cTime - self.pTime)
            self.pTime = cTime
            if img is None:
                return fps
            else:
                cv2.putText(
                    img,
                    f"FPS: {int(fps)}",
                    pos,
                    cv2.FONT_HERSHEY_PLAIN,
                    scale,
                    color,
                    thickness,
                )
                return fps, img
        except ZeroDivisionError:
            return 0
