import cv2
import cv2 as cv
import numpy as np
from PyQt5.QtGui import *
from PyQt5.QtCore import *
import sys
import hsvfilter


class ObjectDetection:

    def __init__(self, threshold, mode, hsv, displayhsv):
        self.Threshold = threshold / 100
        self.Mode = mode
        self.HSV = hsv
        self.DisplayHSV = displayhsv

    def np_to_qimage(self, np, w, h):
        cvImage = cv.cvtColor(np, cv.COLOR_BGR2RGB)
        ConvertToQtFormat = QImage(cvImage.data, cvImage.shape[1], cvImage.shape[0], QImage.Format_RGB888)
        Pic = ConvertToQtFormat.scaled(w, h, Qt.KeepAspectRatio)
        return QPixmap.fromImage(Pic)

    def resize_image(self, image, size):
        w = int(image.shape[1] * size)
        h = int(image.shape[0] * size)
        image = cv.resize(image, (w, h))
        return image

    def get_hsv(self, img):
        hsv = cv.cvtColor(img, cv.COLOR_RGB2HSV)

        h, s, v = cv.split(hsv)

        hsv = cv.merge([h, s, v])

        lowerHSV = np.array([self.HSV.H_Min, self.HSV.S_Min, self.HSV.V_Min])
        upperHSV = np.array([self.HSV.H_Max, self.HSV.S_Max, self.HSV.V_Max])
        maskHSV = cv.inRange(hsv, lowerHSV, upperHSV)

        resultHSV = cv.bitwise_and(hsv, hsv, mask=maskHSV)

        img = cv.cvtColor(resultHSV, cv.COLOR_HSV2RGB)

        return img


    def detect_objects(self, currentImage, objects):


        if self.DisplayHSV:
            currentImage = self.get_hsv(currentImage)

        else:
            return currentImage

        currentImage = self.resize_image(currentImage, 0.5)

        objectImage = objects[0]

        objectImage = self.resize_image(objectImage, 0.5)

        rgbImg = currentImage

        currentImage = cv.cvtColor(currentImage, cv.COLOR_RGB2GRAY)
        objectImage = cv.cvtColor(objectImage, cv.COLOR_RGB2GRAY)

        result = cv.matchTemplate(currentImage, objectImage, cv.TM_CCOEFF_NORMED)
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

                    cv.rectangle(rgbImg, top_left, bottom_right, red, 2, line_type)

                elif self.Mode == "FPS":
                    center_x = x + int(w/2)
                    center_y = y + int(h/2)
                    cv.drawMarker(rgbImg, (center_x, center_y), red, marker_type)

        return rgbImg


