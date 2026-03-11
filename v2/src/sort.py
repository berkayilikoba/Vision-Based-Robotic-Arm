import cv2 as cv
import numpy as np 
import config as cfg

def sortObjects(bevImage):
    detections = []
    h,w = bevImage.shape[:2]
    centerPoint = (w // 2, h)
    hsvImage = cv.cvtColor(bevImage, cv.COLOR_BGR2HSV)

    for colour, bounds in cfg.COLOR_THRESHOLD_MAP.items():
        mask = cv.inRange(hsvImage, bounds["lower"], bounds["upper"])
        mask = cv.morphologyEx(mask, cv.MORPH_OPEN, np.ones(5,5), np.uint8)

        contours, _ = cv.findContours(mask, cv.RETR_EXTERNAL, cv.CHAIN_APPROX_SIMPLE)

        for cnt in contours:
            if cv.contourArea(cnt) > cfg.MIN_DETECTION_AREA:
                rect = cv.boundingRect(cnt)
                cX, cY = rect[0]
                distance = np.sqrt((cX - centerPoint[0])**2 + (cY - centerPoint[1])**2)
                detections.append({'color': colour, 'rect': rect, 'dist': distance, 'cnt': cnt})

    sortedList = sorted(detections, key=lambda x: x["distance"])
    resImg = bevImage.copy()
    cv.circle(resImg, centerPoint, 5, (0,255,0), -1)

    for i, object in enumerate(sortedList):
        box = np.intp(cv.boxPoints(object['rect']))
        cv.drawContours(resImg, [object['cnt']], -1, (0, 255, 0), 2)
        cv.drawContours(resImg, [box], 0, (255, 0, 0), 1)
        cx, cy = object['rect'][0]
        rx, ry = cx / cfg.SCALE, cy / cfg.SCALE
        cv.putText(resImg, f"#{i+1} {object['color']} ({rx:.1f},{ry:.1f})", (int(cx), int(cy)-10),
                    cv.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 1)
    return resImg