import cv2
import numpy as np

REAL_WIDTH = 30.41
REAL_HEIGHT = 21.50
SCALE = 30

pts_src = []
img = None
img_display = None

def select_points(event, x, y, flags, param):
    
    global pts_src, img_display
    if event == cv2.EVENT_LBUTTONDOWN and len(pts_src) < 4:
        pts_src.append([x, y])
        cv2.circle(img_display, (x, y), 7, (0, 255, 0), -1)
        cv2.putText(img_display, str(len(pts_src)), (x+15, y+15), 
                    cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 255, 0), 2)
        cv2.imshow("1. ADIM: KALIBRASYON", img_display)

img_path = 'v2/test-images/mavi1.jpeg' 
img = cv2.imread(img_path)

if img is not None:
    img_display = img.copy()
    cv2.namedWindow("1. ADIM: KALIBRASYON")
    cv2.setMouseCallback("1. ADIM: KALIBRASYON", select_points)
    cv2.imshow("1. ADIM: KALIBRASYON", img_display)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

    if len(pts_src) == 4:
        pts_src_nav = np.array(pts_src, dtype=np.float32)
        bev_w, bev_h = int(REAL_WIDTH * SCALE), int(REAL_HEIGHT * SCALE)
        pts_dst = np.array([[0, 0], [bev_w, 0], [0, bev_h], [bev_w, bev_h]], dtype=np.float32)

        H = cv2.getPerspectiveTransform(pts_src_nav, pts_dst)
        img_bev = cv2.warpPerspective(img, H, (bev_w, bev_h))

        def analyze_blue_object(bev_image):
            hsv = cv2.cvtColor(bev_image, cv2.COLOR_BGR2HSV)
            lower_blue = np.array([100, 150, 50])
            upper_blue = np.array([140, 255, 255])
            mask = cv2.inRange(hsv, lower_blue, upper_blue)
            
            kernel = np.ones((5,5), np.uint8)
            mask = cv2.morphologyEx(mask, cv2.MORPH_OPEN, kernel)
            
            contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
            final_bev = bev_image.copy()

            for cnt in contours:
                if cv2.contourArea(cnt) > 300:
                    rect = cv2.minAreaRect(cnt)
                    box = np.intp(cv2.boxPoints(rect))
                    cv2.drawContours(final_bev, [cnt], -1, (0, 255, 0), 2)
                    cv2.drawContours(final_bev, [box], 0, (255, 0, 0), 1)
                    
                    cx, cy = rect[0]
                    real_x, real_y = cx / float(SCALE), cy / float(SCALE)
                    real_w, real_h = rect[1][0] / float(SCALE), rect[1][1] / float(SCALE)
                    
                    cv2.circle(final_bev, (int(cx), int(cy)), 5, (0, 0, 255), -1)
                    cv2.putText(final_bev, f"X:{real_x:.1f} Y:{real_y:.1f}cm", (int(cx)+10, int(cy)-10),
                                cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 1)
                    cv2.putText(final_bev, f"B:{real_w:.1f}x{real_h:.1f}cm", (int(cx)+10, int(cy)+10),
                                cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 1)
            return final_bev

        result_view = analyze_blue_object(img_bev)
        
        cv2.imwrite('v2/src/test-images/sonuc_kusbakisi.png', result_view)
        print("Görüntü 'v2/src/sonuc_kusbakisi.png' olarak kaydedildi.")

        cv2.imshow("VisionArm-AI V2: Kusbakisi Analiz", result_view)
        cv2.waitKey(0)
        cv2.destroyAllWindows()