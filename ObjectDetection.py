import cv2 as cv
import numpy as np
from win32api import GetSystemMetrics
from Screenshot import Screenshot as ss
import win32api, win32con
from PyQt5.QtGui import *
from PyQt5.QtCore import *

class ObjectDetection:

    def __init__(self, threshold, object):
        self.threshold = threshold
        self.object = object

    def round_threshold(self):
        if self.threshold > 0:
            self.threshold = self.threshold / 100

    def find_object(self):
        screenshot = ss.capture_screen()

        photo_img = cv.imread('Objects/CSGO/csgo.jpg', cv.IMREAD_UNCHANGED)
        object_img = cv.imread('Objects/CSGO/terrorist.jpg', cv.IMREAD_UNCHANGED)

        result = cv.matchTemplate(screenshot, object_img, cv.TM_CCOEFF_NORMED)

        # get best match pos
        min_val, max_val, min_loc, max_loc = cv.minMaxLoc(result)

        ward_w = object_img.shape[1]
        ward_h = object_img.shape[0]

        threshold = self.threshold
        loc = np.where(result >= threshold)

        loc = list(zip(*loc[::-1]))

        rectangles = []
        for l in loc:
            rect = [int(l[0]), int(l[1]), ward_w, ward_h]
            rectangles.append(rect)

        rectangles, weights = cv.groupRectangles(rectangles, 1, 0.5)

        if len(rectangles):
            print("Found images")
            line_color = (255, 0, 0)
            line_type = cv.LINE_4
            marker_color = (0, 0, 255)
            marker_type = cv.MARKER_SQUARE

            for (x, y, w, h) in rectangles:
                top_left = (x, y)
                bottom_right = (x + w, y + h)
                cv.rectangle(photo_img, top_left, bottom_right, marker_color, marker_type)
                win32api.SetCursorPos((x + int(w / 2), y + int(h / 2)))

            cv.imshow('Matches', screenshot)
        else:
            print("No image found")

    def np_to_qimage(self, np, w, h):
        cvImage = cv.cvtColor(np, cv.COLOR_RGB2BGR)

        ConvertToQtFormat = QImage(cvImage.data, cvImage.shape[1], cvImage.shape[0], QImage.Format_RGB888)
        Pic = ConvertToQtFormat.scaled(w, h, Qt.KeepAspectRatio)
        self.screen.setPixmap(QPixmap.fromImage(Pic))