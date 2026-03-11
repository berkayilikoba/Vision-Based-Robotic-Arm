import cv2
import numpy as np

def getHomographyMatrix(ptsSrc, realWidth, realHeight, scale):

    bev_w = int(realWidth * scale)
    bev_h = int(realHeight * scale)
    
    pts_src_nav = np.array(ptsSrc, dtype=np.float32)
    pts_dst = np.array([[0, 0], [bev_w, 0], [0, bev_h], [bev_w, bev_h]], dtype=np.float32)
    H = cv2.getPerspectiveTransform(pts_src_nav, pts_dst)
    return H, (bev_w, bev_h)

def applyPerspective(img, H, size):
    return cv2.warpPerspective(img, H, size)