import time 
import cv2 as cv 
from vision import getColourName
from communication import initArduino, isReady, sendToArduino, closeArduino
from config import CAMERA_INDEX, STABLE_THRESHOLD, REQUIRED_STABLE_TIME

cap = cv.VideoCapture(CAMERA_INDEX)

armWaiting = True
lastCenter = None
stableStartTime = None

if not initArduino():
    print("connection error!")
    exit()

    
while cap.isOpened():
    
    _, frame = cap.read()

    if not armWaiting and isReady():
        armWaiting = True
        print("arm is ready!")

    colour, center = getColourName(frame)

    if armWaiting and colour and center:

        if lastCenter is None or \
            abs(center[0] - lastCenter[0]) > STABLE_THRESHOLD or \
            abs(center[1] - lastCenter[1]) > STABLE_THRESHOLD:
            
            stableStartTime = time.time()
            lastCenter = center

        else:
            elapsed = time.time() - stableStartTime
            cv.putText(frame, f"stabilizing: {max(0, REQUIRED_STABLE_TIME-elapsed):.1f}s", 
                           (20, 40), cv.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 255), 2)
             
            if elapsed >= REQUIRED_STABLE_TIME:
                print(f">> {colour.upper()} stabilized. sending to arduino.")
                sendToArduino(colour)
                armWaiting = False
                lastCenter = None
                stableStartTime = None

    else:
        stableStartTime = None
        lastCenter = None

    cv.imshow("Vision Arm", frame)

    key = cv.waitKey(1)

    if key == ord("q"):
        cv.destroyAllWindows()
        cap.release()
        closeArduino()