import cv2 as cv
import numpy as np 
import math
from config import COLOR_THRESHOLD_MAP, CAMERA_INDEX
import time

prevTime = 0
def fpsCounter(frame):

    global prevTime
    currentTime = time.time()

    fps = 1 / (currentTime - prevTime)
    prevTime = currentTime

    return fps

def getObjectCenterCoordinates(contour):
    
    moments = cv.moments(contour)

    if moments["m00"] != 0:

        centerX = int(moments["m10"] / moments["m00"])
        centerY = int(moments["m01"] / moments["m00"])

        return (centerX, centerY)
    
    return None

def calculateDistanceToCenter(objectX, objectY, cameraW, cameraH):

    cameraCenterX = cameraW // 2
    cameraCenterY = cameraH // 2

    distance = math.sqrt((objectX - cameraCenterX) ** 2 + (objectY - cameraCenterY) ** 2)

    return distance

def processFrame(frame, colourMap):

    height, width = frame.shape[:2]
    detectedBoxes = []

    hsvFrame = cv.cvtColor(frame, cv.COLOR_BGR2HSV)

    for colourName, thresholds in colourMap.items():

        mask = cv.inRange(hsvFrame, thresholds["lower"], thresholds["upper"])
        kernel = np.ones((5,5), np.uint8)
        mask = cv.morphologyEx(mask, cv.MORPH_OPEN, kernel)

        contours, _ = cv.findContours(mask, cv.RETR_EXTERNAL, cv.CHAIN_APPROX_SIMPLE)

        if contours:

            largestContour = max(contours, key = cv.contourArea)

            if cv.contourArea(largestContour) > 1500:
                coordinates = getObjectCenterCoordinates(largestContour)

                if coordinates:

                    distance = calculateDistanceToCenter(coordinates[0], coordinates[1], width, height)

                detectedBoxes.append({
                    "colourName" : colourName,
                    "center" : coordinates,
                    "distance" : distance,
                    "contour" : largestContour
                }) 


    return sorted(detectedBoxes, key = lambda x: x["distance"])

def testOnImage():
    imagePath = "/Users/berkayilikoba/Desktop/Vision-Based-Robotic-Arm/v1/test-images/testImage1.jpeg" 
    frame = cv.imread(imagePath)

    if frame is None:
        print("Error!")

    targets = processFrame(frame, COLOR_THRESHOLD_MAP)

    print(f"number of detected boxes : {len(targets)}")

    for index, target in enumerate(targets):

        cX, cY = target["center"]
        distance = target["distance"]
        name = target["colourName"]

        cv.drawContours(frame, target["contour"], -1, (0,0,0), 3)
        cv.circle(frame, (cX, cY), 5, (0,0,0), -1)
        infoText = f"#{index+1} {name.upper()} (Dist: {int(distance)})"
        cv.putText(frame, infoText, (cX - 20, cY - 20), 
                    cv.FONT_HERSHEY_SIMPLEX, 1.5, (255, 255, 255), 2)
        
    cv.imshow("Test", frame)

    key = cv.waitKey(0)

    if key == ord("q"):
        cv.destroyAllWindows()


def testOnLive():


    cap = cv.VideoCapture(CAMERA_INDEX)
    cap.set(cv.CAP_PROP_FRAME_WIDTH, 1024)
    cap.set(cv.CAP_PROP_FRAME_HEIGHT, 720)

    while cap.isOpened():
        _, frame = cap.read()
        height, width = frame.shape[:2]

        targets = processFrame(frame, COLOR_THRESHOLD_MAP)
        fps = fpsCounter(frame)


        for index, target in enumerate(targets):
            cX, cY = target["center"]
            distance = target["distance"]
            name = target["colourName"]

            if len(targets) > 0:
                countText = f"Detected Boxes: {len(targets)}"
                cv.putText(frame, countText, (20, 40), cv.FONT_HERSHEY_SIMPLEX, 1.7, (0, 255, 255), 5)
                cv.drawContours(frame, target["contour"], -1, (0,0,0), 5)
                cv.circle(frame, (cX, cY), 5, (0,0,0), -1)
                cv.circle(frame, ((width // 2), (height // 2)), 5, (0,255,0), -1)
                infoText = f"#{index+1} {name.upper()} (Dist: {int(distance)})"
                cv.putText(frame, infoText, (cX - 20, cY - 20), 
                            cv.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2)
                fpsText = f"FPS: {int(fps)}"
                cv.putText(frame, fpsText, (20, 70), cv.FONT_HERSHEY_SIMPLEX, 1.7, (0, 255, 0), 5)
                
        cv.imshow("Test on Live", frame)

        key = cv.waitKey(1)

        if key == ord("q"):
            cv.destroyAllWindows()
            cap.release()

        
#testOnImage()

testOnLive()