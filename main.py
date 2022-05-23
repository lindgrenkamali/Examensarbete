import cv2 as cv
import numpy as np
import pyautogui
from win32api import GetSystemMetrics
from Screenshot import Screenshot as ss
import win32api, win32con

screenshot = ss.capture_screen()

cv.imshow('Desktop', screenshot)
cv.waitKey()

w = GetSystemMetrics(0)
h = GetSystemMetrics(1)

farm_img = cv.imread('albion_farm.jpg', cv.IMREAD_UNCHANGED)
cabbage_img = cv.imread('albion_cabbage.jpg', cv.IMREAD_UNCHANGED)
photo_img = cv.imread('csgo.jpg', cv.IMREAD_UNCHANGED)
object_img = cv.imread('terrorist.jpg', cv.IMREAD_UNCHANGED)

result = cv.matchTemplate(photo_img, object_img, cv.TM_CCOEFF_NORMED)

#get best match pos
min_val, max_val, min_loc, max_loc = cv.minMaxLoc(result)

ward_w = object_img.shape[1]
ward_h = object_img.shape[0]

threshold = 0.42
loc = np.where(result >= threshold)

loc = list(zip(*loc[::-1]))
print(loc)

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
        win32api.SetCursorPos((x + int(w/2), y + int(h/2)))

    cv.imshow('Matches', photo_img)
    cv.waitKey()
else:
    print("No image found")