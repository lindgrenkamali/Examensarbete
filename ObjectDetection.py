import cv2
import cv2 as cv
import numpy as np
from PyQt5.QtGui import *
from PyQt5.QtCore import *


class ObjectDetection:

    def __init__(self, threshold, mode):
        self.Threshold = threshold / 100
        self.Mode = mode


    def np_to_qimage(self, np, w, h):
        cvImage = cv.cvtColor(np, cv.COLOR_BGR2RGB)
        ConvertToQtFormat = QImage(cvImage.data, cvImage.shape[1], cvImage.shape[0], QImage.Format_RGB888)
        Pic = ConvertToQtFormat.scaled(w, h, Qt.KeepAspectRatio)
        return QPixmap.fromImage(Pic)

    def detect_objects(self, currentImage, objects):

        currentImage = cv.cvtColor(currentImage, cv.COLOR_RGB2BGR)

        currentImage = cv.cvtColor(currentImage, cv.COLOR_BGR2RGB)

        objectImage = objects[0]

        result = cv.matchTemplate(cv2.cvtColor(currentImage, cv2.COLOR_BGR2GRAY), cv2.cvtColor(objectImage, cv2.COLOR_BGR2GRAY), cv.TM_CCOEFF_NORMED)

        object_w = objectImage.shape[1]
        object_h = objectImage.shape[0]

        results = np.where(result >= self.Threshold)
        locations = list(zip(*results[::-1]))

        rectangles = []
        for l in locations:
            rectangle = [int(l[0]), int(l[1]), object_w, object_h]
            rectangles.append(rectangle)
            rectangles.append(rectangle)

        rectangles, weights = cv.groupRectangles(rectangles, groupThreshold=1, eps=0.5)

        if len(rectangles):

            red = (255, 0, 0)
            line_type = cv.LINE_4
            marker_type = cv.MARKER_CROSS

            for (x, y, w, h) in rectangles:

                if self.Mode == "Default":
                    top_left = (x, y)
                    bottom_right = (x + w, y + h)

                    cv.rectangle(currentImage, top_left, bottom_right, red, 2, line_type)

                elif self.Mode == "FPS":
                    center_x = x + int(w/2)
                    center_y = y + int(h/2)
                    cv.drawMarker(currentImage, (center_x, center_y), red, marker_type)

        return currentImage


