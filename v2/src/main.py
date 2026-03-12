import cv2 as cv
import numpy as np
from utils import detectCorners, getHomographyMatrix

REAL_WIDTH = 30.41
REAL_HEIGHT = 21.50
SCALE = 30

img = cv.imread('v2/test-images/laptopsal.jpeg')

if img is not None:
    centers = detectCorners(img)
    print(len(centers))
    if len(centers) == 4:
        H, (bev_w, bev_h) = getHomographyMatrix(centers, REAL_WIDTH, REAL_HEIGHT, SCALE)
        img_bev = cv.warpPerspective(img, H, (bev_w, bev_h))
        
        hsv = cv.cvtColor(img_bev, cv.COLOR_BGR2HSV)
        mask = cv.inRange(hsv, np.array([53, 255, 0]), np.array([179, 255, 255]))
        
        contours, _ = cv.findContours(mask, cv.RETR_EXTERNAL, cv.CHAIN_APPROX_SIMPLE)
        
        result_view = img_bev.copy()
        for cnt in contours:
            if cv.contourArea(cnt) > 300:
                rect = cv.minAreaRect(cnt)
                box = np.intp(cv.boxPoints(rect))
                cv.drawContours(result_view, [box], 0, (255, 0, 0), 2)
                cx, cy = rect[0]
                cv.putText(result_view, f"X:{cx/SCALE:.1f} Y:{cy/SCALE:.1f}cm", (int(cx), int(cy)),
                           cv.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 1)
        
        cv.imshow("Kusbakisi Analiz", result_view)
        cv.imshow("masked", mask)

        cv.waitKey(0)
    else:
        print(f"Hata: 4 kosse bulunamadi. Tespit edilen: {len(centers)}")
    
    cv.destroyAllWindows()