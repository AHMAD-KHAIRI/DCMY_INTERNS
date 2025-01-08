import sys
sys.dont_write_bytecode = True

import cv2
from aruco_object_detector import *
import numpy as np

# load aruco detector
parameters = cv2.aruco.DetectorParameters()
aruco_dict = cv2.aruco.getPredefinedDictionary(cv2.aruco.DICT_5X5_50)
# aruco_dict = cv2.aruco.Dictionary(cv2.aruco.DICT_5X5_50, 13)

# load object detector
detector = HomogeneousBgDetector()

# load image
img = cv2.imread("./images/phone_aruco_marker.jpg")

# get aruco marker
corners, _, _ = cv2.aruco.detectMarkers(img, aruco_dict, parameters=parameters)

# draw polygon arround the marker
int_corners = np.int_(corners)
cv2.polylines(img, int_corners, True, (0, 255, 0), 5)

# aruco perimeter
aruco_perimeter = cv2.arcLength(corners[0], True)

# pixel to cm ratio
pixel_cm_ratio = aruco_perimeter / 21


contours = detector.detect_objects(img)

# draw objects boundaries
for cnt in contours:

    # get rect
    rect = cv2.minAreaRect(cnt)
    (x, y),(w, h), angle = rect

    # get width and height of the objects by applying the ratio pixel to cm
    object_width = w / pixel_cm_ratio
    object_height = h / pixel_cm_ratio

    # display rectangle
    box = cv2.boxPoints(rect)
    box = np.int_(box)

    cv2.circle(img, (int(x), int(y)), 5, (0, 0, 255), -1)
    cv2.polylines(img, [box], True, (255, 0, 0), 2)
    cv2.putText(img, "Width {} cm".format(round(object_width, 1)), (int(x - 100), int(y - 15)), cv2.FONT_HERSHEY_PLAIN, 2, (100, 200, 0), 2)
    cv2.putText(img, "Height {} cm".format(round(object_height, 1)), (int(x - 100), int(y + 15)), cv2.FONT_HERSHEY_PLAIN, 2, (100, 200, 0), 2)

cv2.imshow("Image", img)
cv2.waitKey(0)