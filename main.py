import ObjectDetectionInterface
import cascadetrainer
from PhotoManager import PhotoManager
import cv2
import tracemalloc

ObjectDetectionInterface.run_objectdetection()

cv2.imshow("Test", PhotoManager.capture_screen())
cv2.waitKey()

cascadetrainer.negative_files()