# Official script [officialv6.py]
# WORKING VERSION WITH [serverv3.py]
VERSION = 'officialv7.py'

# Import Libraries
import numpy as np
import cv2
import os
#import imutils
import time
import datetime
import json

import sys
import socket
import tkinter as tk
# import random
# import math

# from PIL import Image, ImageTk

from _thread import *
import threading

import calibration

if len(sys.argv) != 2:
    print("Usage: python3 officialv7.py <hostID>")
    sys.exit(1)

HOST = sys.argv[1]
PORT = 8009

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((HOST, PORT))

#define the webcam used
webcam = cv2.VideoCapture(0,cv2.CAP_DSHOW)

#check for compatibility. If not, force search the webcam
_, frame = webcam. read()

try:
    if frame == None:
        webcam = cv2.VideoCapture(-1)
except:
    print("Webcam Detected First Try.")

set = True
print("Starting in 3 seconds... \n3")
time.sleep(1)
print("2")
time.sleep(1)
print("1")
time.sleep(1)
print("Collecting Data")
start = time.time()
count = 0
while(set):

    # Grabbing frame from webcam
    _, frame = webcam.read()


    # Apply Grayscale
    grayscale = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    # Apply Gaussian Blur
    blur = cv2.GaussianBlur(grayscale, (9,9), 0)

        #Create the Mask / Threshold
    maskThresh = cv2.adaptiveThreshold(blur, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C,cv2.THRESH_BINARY_INV,23,3)

    #HSV
    # Convert the BGR image to HSV image.
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

    #creating the ranges for our set colors
    
    red_lower_range = np.array([0, 255, 130])
    red_upper_range = np.array([180, 255, 255])
    red_mask = cv2.inRange(hsv,red_lower_range,red_upper_range)

    yellow_lower_range = np.array([10, 58, 180])
    yellow_upper_range = np.array([35, 255, 255])
    yellow_mask = cv2.inRange(hsv,yellow_lower_range,yellow_upper_range)

    green_lower_range = np.array([36, 25, 25])
    green_upper_range = np.array([70, 255, 255])
    green_mask = cv2.inRange(hsv,green_lower_range,green_upper_range)

    purple_lower_range = np.array([116, 170, 70])
    purple_upper_range = np.array([143, 255, 255])
    purple_mask = cv2.inRange(hsv,purple_lower_range,purple_upper_range)

    #creating the mask for the colors
    ary1 = np.ones((5,5),"uint8")

    red_mask = cv2.dilate(red_mask,ary1)  
    res_red = cv2.bitwise_and(frame,frame,mask = red_mask)

    yellow_mask = cv2.dilate(yellow_mask,ary1)  
    res_yellow = cv2.bitwise_and(frame,frame,mask = yellow_mask)

    green_mask = cv2.dilate(green_mask,ary1)  
    res_green = cv2.bitwise_and(frame,frame,mask = green_mask)

    purple_mask = cv2.dilate(purple_mask,ary1)  
    res_purple = cv2.bitwise_and(frame,frame,mask = purple_mask)

    #creating contour for red
    contours,top = cv2.findContours(red_mask,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)

    for camera, contour in enumerate(contours):
        area = cv2.contourArea(contour)
        if area > 300: 
            x,y,width,height = cv2.boundingRect(contour)
            frame = cv2.rectangle(frame,(x,y),(x+width,y+height),(0,0,225),2)
            cv2.putText(frame, "RED", (x,y),cv2.FONT_HERSHEY_SIMPLEX,1.0,(0,0,255))
            print("stop")
            count += 1
        if count == 100:
            set = False

    #creating contour for yellow
    contours,top = cv2.findContours(yellow_mask,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)

    for camera, contour in enumerate(contours):
        area = cv2.contourArea(contour)
        if area > 300: 
            x,y,width,height = cv2.boundingRect(contour)
            frame = cv2.rectangle(frame,(x,y),(x+width,y+height),(0,225,225),2)
            cv2.putText(frame, "Yellow", (x,y),cv2.FONT_HERSHEY_SIMPLEX,1.0,(0,225,255))
            print("slow")

    #creating contour for green
    contours,top = cv2.findContours(green_mask,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)

    for camera, contour in enumerate(contours):
        area = cv2.contourArea(contour)
        if area > 300: 
            x,y,width,height = cv2.boundingRect(contour)
            frame = cv2.rectangle(frame,(x,y),(x+width,y+height),(0,225,0),2)
            cv2.putText(frame, "Green", (x,y),cv2.FONT_HERSHEY_SIMPLEX,1.0,(0,225,0))
            print("go")


    #creating contour for purple
    contours,top = cv2.findContours(purple_mask,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)

    for camera, contour in enumerate(contours):
        area = cv2.contourArea(contour)
        if area > 300: 
            x,y,width,height = cv2.boundingRect(contour)
            frame = cv2.rectangle(frame,(x,y),(x+width,y+height),(238,130,238),2)
            cv2.putText(frame, "Purple", (x,y),cv2.FONT_HERSHEY_SIMPLEX,1.0,(238,130,238))
            print("reverse")                                


    #Close the Windows Ctrl+C
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
    #Displaying the Frame
    cv2.imshow('Test',frame)
    #cv2.imshow("mask",maskThresh)

# Safely close all windows
webcam.release()
cv2.destroyAllWindows()

print("My program took", time.time() - start, "seconds to run")