import mss
import numpy as np
import cv2 as cv
import mss.windows
mss.windows.CAPTUREBLT = 0

class PhotoManager:
    @staticmethod
    def capture_screen():
        with mss.mss() as mss_instance:
            monitor = mss_instance.monitors[1]
            screenshot = mss_instance.grab(monitor)
            nparray = np.array(screenshot)
            return nparray

    @staticmethod
    def path_to_cvimage(filepath):
        return cv.imread(filepath, cv.IMREAD_UNCHANGED)
