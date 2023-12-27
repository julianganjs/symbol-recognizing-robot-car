import cv2
import numpy as np
from scipy.stats import itemfreq
import os
import RPi.GPIO as GPIO
from time import sleep

ena = 23
in1 = 24
in2 = 25
in3 = 12
in4 = 16
enb = 20

GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)

GPIO.setup(ena,GPIO.OUT)
GPIO.setup(in1,GPIO.OUT)
GPIO.setup(in2,GPIO.OUT)
GPIO.setup(enb,GPIO.OUT)
GPIO.setup(in3,GPIO.OUT)
GPIO.setup(in4,GPIO.OUT)

GPIO.output(in1,GPIO.LOW)
GPIO.output(in2,GPIO.LOW)
GPIO.output(in3,GPIO.LOW)
GPIO.output(in4,GPIO.LOW)

#PWM
P1 = GPIO.PWM(ena, 255)
P2 = GPIO.PWM(enb, 255)
P1.start(30)
P2.start(27)


travel = 0
end = 0
start = 0

countf = 0
countl = 0
countr = 0
countb = 0

#Motor Movement
def move_forward():    
    GPIO.output(in1, GPIO.HIGH)
    GPIO.output(in2, GPIO.LOW)
    GPIO.output(in3, GPIO.HIGH)
    GPIO.output(in4, GPIO.LOW )
    sleep(1.0)

def move_backwards():
    GPIO.output(in1, GPIO.LOW)
    GPIO.output(in2, GPIO.HIGH)
    GPIO.output(in3, GPIO.LOW)
    GPIO.output(in4, GPIO.HIGH)
    sleep(1)

def turn_left():
    GPIO.output(in1, GPIO.HIGH)
    GPIO.output(in2, GPIO.LOW)
    GPIO.output(in3, GPIO.HIGH)
    GPIO.output(in4, GPIO.LOW)
    sleep(0.3)
    P2.ChangeDutyCycle(52)
    GPIO.output(in1, GPIO.LOW)
    GPIO.output(in2, GPIO.LOW)
    GPIO.output(in3, GPIO.HIGH)
    GPIO.output(in4, GPIO.LOW)
    sleep(0.75)
    P2.ChangeDutyCycle(27)
    GPIO.output(in1, GPIO.HIGH)
    GPIO.output(in2, GPIO.LOW)
    GPIO.output(in3, GPIO.HIGH)
    GPIO.output(in4, GPIO.LOW)
    sleep(0.3)
    

def turn_right():
    GPIO.output(in1, GPIO.HIGH)
    GPIO.output(in2, GPIO.LOW)
    GPIO.output(in3, GPIO.HIGH)
    GPIO.output(in4, GPIO.LOW)
    sleep(0.3)
    P1.ChangeDutyCycle(50)
    GPIO.output(in1, GPIO.HIGH)
    GPIO.output(in2, GPIO.LOW)
    GPIO.output(in3, GPIO.LOW)
    GPIO.output(in4, GPIO.LOW)
    sleep(0.75)
    P1.ChangeDutyCycle(30)
    GPIO.output(in1, GPIO.HIGH)
    GPIO.output(in2, GPIO.LOW)
    GPIO.output(in3, GPIO.HIGH)
    GPIO.output(in4, GPIO.LOW)
    sleep(0.3)

def no_movement():
    GPIO.output(in1, GPIO.LOW)
    GPIO.output(in2, GPIO.LOW)
    GPIO.output(in3, GPIO.LOW)
    GPIO.output(in4, GPIO.LOW)

def get_dominant_color(image, n_colors):
    pixels = np.float32(image).reshape((-1, 3))
    criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 200, .1)
    flags = cv2.KMEANS_RANDOM_CENTERS
    flags, labels, centroids = cv2.kmeans(
        pixels, n_colors, None, criteria, 10, flags)
    palette = np.uint8(centroids)
    return palette[np.argmax(itemfreq(labels)[:, -1])]


clicked = False
def onMouse(event, x, y, flags, param):
    global clicked
    if event == cv2.EVENT_LBUTTONUP:
        clicked = True

def arrow(frame):
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    # define range of blue color in HSV
    lower_blue = np.array([90,130,40])
    upper_blue = np.array([160,255,150])
    # Threshold the HSV image to get only blue colors
    img5 = cv2.inRange(hsv, lower_blue, upper_blue)
    circles = cv2.HoughCircles(img5, cv2.HOUGH_GRADIENT,
                                1, 50, param1=120, param2=40)

    if not circles is None:
        circles = np.uint16(np.around(circles))
        max_r, max_i = 0, 0
        for i in range(len(circles[:, :, 2][0])):
            if circles[:, :, 2][0][i] > 50 and circles[:, :, 2][0][i] > max_r:
                max_i = i
                max_r = circles[:, :, 2][0][i]
        x, y, r = circles[:, :, :][0][max_i]
        if y > r and x > r:
            square = frame[y-r:y+r, x-r:x+r]

            dominant_color = get_dominant_color(square, 2)
            if dominant_color[2] > 100:
                print("STOP")
            elif dominant_color[0] > 80:
                zone_0 = square[square.shape[0]*3//8:square.shape[0]
                                * 5//8, square.shape[1]*1//8:square.shape[1]*3//8]
                zone_0_color = get_dominant_color(zone_0, 1)

                zone_1 = square[square.shape[0]*1//8:square.shape[0]
                                * 3//8, square.shape[1]*3//8:square.shape[1]*5//8]
                zone_1_color = get_dominant_color(zone_1, 1)

                zone_2 = square[square.shape[0]*3//8:square.shape[0]
                                * 5//8, square.shape[1]*5//8:square.shape[1]*7//8]
                zone_2_color = get_dominant_color(zone_2, 1)

                zone_3 = square[square.shape[0]*5//8:square.shape[0]
                                * 7//8, square.shape[1]*3//8:square.shape[1]*5//8]
                zone_3_color = get_dominant_color(zone_3, 1)

                if zone_1_color[2] < 60:
                    if sum(zone_0_color) > sum(zone_2_color):
                        global countr
                        if countr == 0:
                            cv2.putText(frame,"RIGHT",(50,50),cv2.FONT_HERSHEY_COMPLEX,1,(255,0,255),2)
                            turn_right()
                            countr += 1
                    else:
                        global countl
                        if countl == 0:
                            cv2.putText(frame,"LEFT",(50,50),cv2.FONT_HERSHEY_COMPLEX,1,(255,0,255),2)
                            turn_left()
                            countl += 1
                else:
                    if sum(zone_1_color) > sum(zone_0_color) and sum(zone_1_color) > sum(zone_2_color) and sum(zone_3_color) > sum(zone_1_color):
                        global countb
                        if countb == 0:
                            cv2.putText(frame,"BACKWARDS",(50,50),cv2.FONT_HERSHEY_COMPLEX,1,(255,0,255),2)
                            move_backwards()
                            countb += 1
                    elif sum(zone_1_color) > sum(zone_3_color):
                        global countf
                        if countf == 0:
                            cv2.putText(frame,"FORWARD",(50,50),cv2.FONT_HERSHEY_COMPLEX,1,(255,0,255),2)
                            move_forward(
                            countf += 1
                return 0
    else:
        return 1


def stop(ROI,frame):
    
    hsv = cv2.cvtColor(ROI, cv2.COLOR_BGR2HSV)
    lower_red = np.array([-8,120,50])
    upper_red = np.array([15,195,160])
    img2 = cv2.inRange(hsv, lower_red, upper_red)
    circles = cv2.HoughCircles(img2, cv2.HOUGH_GRADIENT,
                                1, 50, param1=120, param2=40)
    if not circles is None:
        cv2.putText(frame,"STOP",(50,50),cv2.FONT_HERSHEY_COMPLEX,1,(255,0,255),2)
        no_movement()
        return 1
    else:
        return 0


def distance_stop(frame):
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    lower_red = np.array([-15,180,70])
    upper_red = np.array([15,255,210])
    img2 = cv2.inRange(hsv, lower_red, upper_red)
    #cv2.imshow('cameadws',img2)
    circles = cv2.HoughCircles(img2, cv2.HOUGH_GRADIENT,
                                        1, 50, param1=10, param2=10)
    if not circles is None:
        if start == 1:
            T = str(travel)
            cv2.putText(frame,"Distance:",(50,50),cv2.FONT_HERSHEY_COMPLEX,1,(255,0,255),2)
            cv2.putText(frame,T,(220,50),cv2.FONT_HERSHEY_COMPLEX,1,(255,0,255),2)
            cv2.putText(frame,"cm",(290,50),cv2.FONT_HERSHEY_COMPLEX,1,(255,0,255),2)
            for i in circles[0, :]:
                cv2.circle(frame, (i[0], i[1]), i[2], (0, 255, 0), 2)
                cv2.circle(frame, (i[0], i[1]), 2, (0, 0, 255), 3)
            return 1
        elif start == 0:
            cv2.putText(frame,"No Distance",(50,50),cv2.FONT_HERSHEY_COMPLEX,1,(255,0,255),2)
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
            move_forward()
            global start
            start = 1
            global travel
            travel += 9.5
            return 1
        else:
            return 0
    else:
        return 0

def shapes(frame):
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    lower_orange = np.array([7,80,60])
    upper_orange = np.array([40,255,240])
    img3 = cv2.inRange(hsv, lower_orange, upper_orange)
    img4=img3.copy()
    #cv2.imshow('camedara',img4)
    x,y,w,h = cv2.boundingRect(img4)
    
    if x>10 or y>10 or h>10:
        kernel = np.ones((5,5), np.uint8)
        mask = cv2.erode(img3, kernel)
        contours, _ = cv2.findContours(mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)[-2:]
  
        i = 0
        font = cv2.FONT_HERSHEY_COMPLEX

        for contour in contours:

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

    



cameraCapture = cv2.VideoCapture(0)
#cameraCapture.set(cv2.CAP_PROP_FRAME_WIDTH, 320)
#cameraCapture.set(cv2.CAP_PROP_FRAME_HEIGHT, 200)

while True:
    
    success, frame = cameraCapture.read()
    frame = cv2.flip(frame, 0)
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    lower_purple = np.array([110,60,5])
    upper_purple = np.array([195,200,130])
    # Threshold the HSV image to get only blue colors
    img3 = cv2.inRange(hsv, lower_purple, upper_purple)
    img4=img3.copy()
    x,y,w,h = cv2.boundingRect(img4)
    no_movement()
    
    if x>10 or y>10 or h>10:
        if ((y+h)/(x+w))>0.6 and ((y+h)/(x+w))<0.67:
            ROI = frame[y:y+h, x:x+w]
            cv2.rectangle(frame, (x, y), (x+w, y+h), (255,0,0), 2)
            flag = 0
            if end == 0:
                flag = arrow(frame)
                if flag == 1:
                    end = stop(ROI,frame)

            elif end == 1:
                flag1 = distance_start(ROI)
                if flag1 == 0:
                    flag2 = distance_stop(ROI)
                    if flag2 == 0:
                        shapes(ROI)
                

    cv2.imshow('camera',frame)
    cv2.waitKey(1)
