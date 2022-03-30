import numpy as np
import cv2


class ShowImage(object):
    def __init__(self, frame, kernel):
        self.frame = frame
        self.kernel = kernel
        self.hsv = cv2.cvtColor(self.frame, cv2.COLOR_BGR2HSV)
        self.mask_blue = cv2.inRange(self.hsv, np.array([96, 0, 0]), np.array([118, 255, 255]))
        self.mask_green = cv2.inRange(self.hsv, np.array([52, 0, 0]), np.array([89, 255, 243]))
        self.mask_yellow = cv2.inRange(self.hsv, np.array([0, 125, 201]), np.array([35, 255, 255]))

    def show_image(self):
        self._completion_all_mask()
        mask = cv2.inRange(self.hsv, np.array([0, 0, 77]), np.array([0, 0, 255]))
        opening = cv2.morphologyEx(mask, cv2.MORPH_OPEN, self.kernel)
        closing = cv2.morphologyEx(opening, cv2.MORPH_CLOSE, self.kernel)

        cv2.imshow("yellow", self.mask_yellow)
        cv2.imshow("blue_dots", self.mask_blue)
        cv2.imshow("green", self.mask_green)
        cv2.imshow("walls", closing)
        cv2.imshow("frame", self.frame)
        cv2.waitKey(3)

    def _completion_all_mask(self):
        self._completion_mask(self.mask_blue)
        self._completion_mask(self.mask_blue)
        self._completion_mask(self.mask_blue)

    def _completion_mask(self, mask):
        _, contours, _ = mask
        self._completion_frame(contours, 0, 255, 0)

    def _completion_frame(self, contours, r, g, b):
        for x in range(len(contours)):
            area = cv2.contourArea(contours[x])
            if area > 5:
                x, y, w, h = cv2.boundingRect(contours[x])
                self.frame = cv2.rectangle(self.frame, (x, y), (x + w, y + h), (r, g, b), 2)
