import cv2
import time
import numpy as np

def nothing(x):
    pass

#define the webcam used
webcam = cv2.VideoCapture(0,cv2.CAP_DSHOW)

#check for compatibility. If not, force search the webcam
_, frame = webcam. read()

#create the trackbars 
#cv2.namedWindow("Trackbars")

# Now create 6 trackbars that will control the lower and upper range of 
# H,S and V channels. The Arguments are like this: Name of trackbar, 
# window name, range,callback function. For Hue the range is 0-179 and
# for S,V its 0-255.
# cv2.createTrackbar("L - H", "Trackbars", 0, 179, nothing)
# cv2.createTrackbar("L - S", "Trackbars", 0, 255, nothing)
# cv2.createTrackbar("L - V", "Trackbars", 0, 255, nothing)
# cv2.createTrackbar("U - H", "Trackbars", 179, 179, nothing)
# cv2.createTrackbar("U - S", "Trackbars", 255, 255, nothing)
# cv2.createTrackbar("U - V", "Trackbars", 255, 255, nothing)


try: 
    if frame == None:
        webcam = cv2.VideoCapture(-1)
except:
    print("Webcam is Detected.")

while(True):
    #grab info from the webcam
    _, frame = webcam.read()

    #Applying the grayscale
    grayscale = cv2.cvtColor(frame,cv2.COLOR_BGR2GRAY)

    #Apply Gaussian Blur
    blur = cv2.GaussianBlur(grayscale,(9,9),0)

    #Create the Mask / Threshold
    maskThresh = cv2.adaptiveThreshold(blur, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C,cv2.THRESH_BINARY_INV,23,3)

    #HSV
    # Convert the BGR image to HSV image.
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

    #creating the ranges for our set colors
    
    red_lower_range = np.array([0, 200, 189])
    red_upper_range = np.array([180, 255, 255])
    red_mask = cv2.inRange(hsv,red_lower_range,red_upper_range)

    yellow_lower_range = np.array([0, 125, 180])
    yellow_upper_range = np.array([70, 180, 255])
    yellow_mask = cv2.inRange(hsv,yellow_lower_range,yellow_upper_range)

    green_lower_range = np.array([60, 60, 60])
    green_upper_range = np.array([86, 255, 255])
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



webcam.release()
cv2.destroyAllWindows()