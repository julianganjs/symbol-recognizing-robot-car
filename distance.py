import cv2
import pytesseract
import numpy as np


cameraCapture = cv2.VideoCapture(0)

def distance_stop(frame):
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    lower_red = np.array([-7,110,110])
    upper_red = np.array([17,195,233])
    img2 = cv2.inRange(hsv, lower_red, upper_red)
    #cv2.imshow('cameadws',img2)
    circles = cv2.HoughCircles(img2, cv2.HOUGH_GRADIENT,
                                        1, 50, param1=20, param2=13)
    if not circles is None:
        cv2.putText(frame,"Distance Stop",(50,50),cv2.FONT_HERSHEY_COMPLEX,1,(255,0,255),2)
        for i in circles[0, :]:
            cv2.circle(frame, (i[0], i[1]), i[2], (0, 255, 0), 2)
            cv2.circle(frame, (i[0], i[1]), 2, (0, 0, 255), 3)

        return 1
    else:
        return 0


def distance_start(frame):
    
    hsv = cv2.cvtColor(frame,cv2.COLOR_BGR2HSV)
    lower_green = np.array([60,80,50])
    upper_green = np.array([80,255,180])
    img3 = cv2.inRange(hsv, lower_green, upper_green)
    img4=img3.copy()
    x,y,w,h = cv2.boundingRect(img4)
    if x>10 or y>10 or h>10:
        if ((y+h)/(x+w))>1.85 and ((y+h)/(x+w))<=2.1:
            cv2.rectangle(frame, (x, y), (x+w, y+h), (255,0,0), 2)
            cv2.putText(frame,"Distance Start",(50,50),cv2.FONT_HERSHEY_COMPLEX,1,(255,0,255),2)
            return 1
        else:
            return 0
    else:
        return 0


while True:

    flag = 0
    flag1 = 0
    success, frame = cameraCapture.read()
    frame = cv2.flip(frame, 0)
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    lower_purple = np.array([140,60,5])
    upper_purple = np.array([175,200,120])
    img3 = cv2.inRange(hsv, lower_purple, upper_purple)
    img4=img3.copy()
    x,y,w,h = cv2.boundingRect(img4)

    if x>10 or y>10 or h>10:
        if ((y+h)/(x+w))>0.6 and ((y+h)/(x+w))<0.67:
            ROI = frame[y:y+h, x:x+w]
            cv2.rectangle(frame, (x, y), (x+w, y+h), (255,0,0), 2)
            flag = distance_stop(ROI)
            if flag == 0:
                flag1 = distance_start(ROI)   


    cv2.imshow('camera',frame)
    cv2.waitKey(1)
