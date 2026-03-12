import cv2 as cv
import numpy as np
import config as cfg

def getHomographyMatrix(ptsSrc, realWidth, realHeight, scale):

    bev_w = int(realWidth * scale)
    bev_h = int(realHeight * scale)
    
    pts_src_nav = np.array(ptsSrc, dtype=np.float32)
    pts_dst = np.array([[0, 0], [bev_w, 0], [0, bev_h], [bev_w, bev_h]], dtype=np.float32)
    H = cv.getPerspectiveTransform(pts_src_nav, pts_dst)
    return H, (bev_w, bev_h)

def applyPerspective(img, H, size):
    return cv.warpPerspective(img, H, size)

def sortObjects(bevImage):

    hsvImage = cv.cvtColor(bevImage, cv.COLOR_BGR2HSV)
    detections = []
    h, w = hsvImage.shape[:2]
    centerPoint = (w // 2, h // 2)
    
    for colour, bounds in cfg.COLOR_THRESHOLD_MAP.items():

        mask = cv.inRange(hsvImage, bounds["lower"], bounds["upper"])
        mask = cv.morphologyEx(mask, cv.MORPH_OPEN, np.ones((5,5), np.uint8))
        contours, _ = cv.findContours(mask, cv.RETR_EXTERNAL, cv.CHAIN_APPROX_SIMPLE)

        for cnt in contours:

            if cv.contourArea(cnt) >= cfg.MIN_DETECTION_AREA:
                
                x, y, ww, hh = cv.boundingRect(cnt)
                obj_cx = x + (ww // 2)
                obj_cy = y + (hh // 2)

                distance = np.sqrt((obj_cx - centerPoint[0])**2 + (obj_cy - centerPoint[1])**2)
                
                detections.append({
                    "colour": colour,
                    "rect": (x, y, ww, hh),
                    "cnt": cnt,
                    "dst": distance
                })                

    sortedList = sorted(detections, key=lambda x: x["dst"])
    resImg = bevImage.copy()
    cv.circle(resImg, centerPoint, 5, (0, 255, 0), -1)

    for i, obj in enumerate(sortedList):
        x, y, ww, hh = obj['rect']
        cv.drawContours(resImg, [obj['cnt']], -1, (0, 255, 0), 2)
        
        text = f"#{i+1} {obj['colour']} Dist:{obj['dst']:.1f}"
        cv.putText(resImg, text, (x, y - 10),
                    cv.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 1)

    return resImg


import cv2 as cv
import numpy as np

def orderCorners(pts):
    pts = np.array(pts, dtype="float32")
    rect = np.zeros((4, 2), dtype="float32")
    s = pts.sum(axis=1)
    rect[0] = pts[np.argmin(s)] 
    rect[3] = pts[np.argmax(s)] 
    diff = np.diff(pts, axis=1)
    rect[1] = pts[np.argmin(diff)] 
    rect[2] = pts[np.argmax(diff)] 
    return rect

def getHomographyMatrix(ptsSrc, realWidth, realHeight, scale):
    bev_w = int(realWidth * scale)
    bev_h = int(realHeight * scale)
    pts_src_ordered = orderCorners(ptsSrc)
    pts_dst = np.array([[0, 0], [bev_w, 0], [0, bev_h], [bev_w, bev_h]], dtype=np.float32)
    H = cv.getPerspectiveTransform(pts_src_ordered, pts_dst)
    return H, (bev_w, bev_h)

def detectCorners(frame):

    gray = cv.cvtColor(frame, cv.COLOR_BGR2GRAY)
    _, thresh = cv.threshold(gray, 50, 255, cv.THRESH_BINARY_INV)
    contours, _ = cv.findContours(thresh, cv.RETR_EXTERNAL, cv.CHAIN_APPROX_SIMPLE)
    markedCenters = []

    for cnt in contours:

        area = cv.contourArea(cnt)

        if 100 < area < 10000:

            M = cv.moments(cnt)

            if M["m00"] != 0:

                cX = int(M["m10"] / M["m00"])
                cY = int(M["m01"] / M["m00"])
                markedCenters.append((cX, cY))

    cv.imshow("asd", gray)
    key = cv.waitKey(0)
    if key == ord("q"):
        cv.destroyAllWindows()           
    return markedCenters

def orderCorners(pts):

    pts = np.array(pts, dtype="float32")
    rect = np.zeros((4, 2), dtype="float32")

    s = pts.sum(axis=1)
    rect[0] = pts[np.argmin(s)] 
    rect[3] = pts[np.argmax(s)] 

    diff = np.diff(pts, axis=1)
    rect[1] = pts[np.argmin(diff)] 
    rect[2] = pts[np.argmax(diff)] 
    
    return rect
