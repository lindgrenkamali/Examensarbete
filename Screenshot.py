import mss
import numpy as np
import cv2 as cv
import mss.windows
from PyQt5 import QtGui
from PIL import Image
from PIL.ImageQt import ImageQt
mss.windows.CAPTUREBLT = 0
import time


class Screenshot:
    @staticmethod
    def capture_screen():
        with mss.mss() as mss_instance:
            monitor = mss_instance.monitors[1]
            screenshot = mss_instance.grab(monitor)
            nparray = np.array(screenshot)
            return nparray
