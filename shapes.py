import cv2
import numpy as np
from scipy.stats import itemfreq
import os

cameraCapture = cv2.VideoCapture(0)

while True:
    
    success, frame = cameraCapture.read()
    frame = cv2.flip(frame, 0)
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    lower_purple = np.array([10,130,50])
    upper_purple = np.array([40,235,190])
    # Threshold the HSV image to get only blue colors
    img3 = cv2.inRange(hsv, lower_purple, upper_purple)
    img4=img3.copy()
    x,y,w,h = cv2.boundingRect(img4)
    
    
    
    if x>10 or y>10 or h>10:/
        if True:
            kernel = np.ones((5,5), np.uint8)
            mask = cv2.erode(img3, kernel)
            contours, _ = cv2.findContours(mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)[-2:]
  
            i = 0
            font = cv2.FONT_HERSHEY_COMPLEX

            for contour in contours:
                if i == 0:
                    i = 1
                    continue

                approx = cv2.approxPolyDP(contour, 0.04 * cv2.arcLength(contour, True), True)
                x = approx.ravel() [0]
                y = approx.ravel() [1]

                cv2.drawContours(frame, [approx], 0, (0, 0, 255), 5)
  
              
                if len(approx) == 3:
                    cv2.putText(frame, "Triangle", (x, y), font, 0.5, (0,0,0))
                elif len(approx) == 4:
                    cv2.putText(frame, "Rectangle", (x, y), font, 0.5, (0,0,0))
                else:
                    cv2.putText(frame, "Circle", (x, y), font, 1, (0,0,0))

    
    cv2.imshow('camera',frame)
    cv2.waitKey(1)
