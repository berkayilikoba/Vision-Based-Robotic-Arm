import cv2 as cv 
import numpy as np 
from config import MIN_DETECTION_AREA, COLOR_THRESHOLD_MAP, TEST_IMAGES_DIR, CAMERA_INDEX
import os 


def getTestImages(filename):
    return os.path.join(TEST_IMAGES_DIR, filename)


def getColourName(frame, imshow = False):

    hsvFrame = cv.cvtColor(frame, cv.COLOR_BGR2HSV)

    detectedColour = None
    maxArea = 0
    bestContour = None
    center = None, None

    for name, limits in COLOR_THRESHOLD_MAP.items():

        mask = cv.inRange(hsvFrame, limits["lower"], limits["upper"])

        mask = cv.erode(mask, None, iterations=2)
        mask = cv.dilate(mask, None, iterations=2)

        contours, _ = cv.findContours(mask, cv.RETR_EXTERNAL, cv.CHAIN_APPROX_SIMPLE)

        for cnt in contours:

            area = cv.contourArea(cnt)



            if area > MIN_DETECTION_AREA and area > maxArea:
                maxArea = area
                detectedColour = name
                bestContour = cnt

        if detectedColour is not None and bestContour is not None:
            cv.drawContours(frame, [bestContour], -1, (0,255,0), 5)
            infoText = f"{detectedColour.upper()} | Area: {int(maxArea)}"
            cv.putText(frame, infoText, (50, 20), 
                        cv.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 255), 2)
            
            M = cv.moments(bestContour)

            if M["m00"] != 0:
                cX = int(M["m10"] / M["m00"])
                cY = int(M["m01"] / M["m00"])
                center = (cX, cY)
                cv.drawContours(frame, [bestContour], -1, (0, 255, 0), 5)
                cv.circle(frame, center, 5, (255, 255, 255), -1)

    return detectedColour, center


def testOnImage():  

    path = getTestImages("redCube1.jpeg")

    image = cv.imread(path)

    clr, (cx,cy) = getColourName(image)
    

    if clr is not None:
        print(clr)
        print(cx)
        print(cy)
    cv.imshow("Image", image)

    key = cv.waitKey(0)

    if key == ord("q"):
        cv.destroyAllWindows()

#testOnImage()

def testOnLive():
    cap = cv.VideoCapture(CAMERA_INDEX)

    while cap.isOpened():

        _, frame = cap.read()

        clr, (cx,cy) = getColourName(frame)

        if clr is not None:
            print(clr)

        cv.imshow("Frame", frame)

        key = cv.waitKey(1)

        if key == ord("q"):
            cv.destroyAllWindows()
            cap.release()

testOnLive()