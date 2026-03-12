import cv2 as cv
import numpy as np
import os
from config import COLOR_THRESHOLD_MAP, CAMERA_INDEX

def updateConfigFile(colorName, lowerThreshold, upperThreshold):
    configPath = os.path.join(os.path.dirname(__file__), "config.py")
    COLOR_THRESHOLD_MAP[colorName]["lower"] = lowerThreshold
    COLOR_THRESHOLD_MAP[colorName]["upper"] = upperThreshold
    
    with open(configPath, "w", encoding="utf-8") as configFile:
        configFile.write("import numpy as np\n\n")
        configFile.write(f"CAMERA_INDEX = {CAMERA_INDEX}\n")
        configFile.write("ARDUINO_SERIAL_PORT = '/dev/cu.usbmodem1101'\n")
        configFile.write("BAUD_RATE_SPEED = 9600\n\n")
        configFile.write("COLOR_THRESHOLD_MAP = {\n")
        for key, value in COLOR_THRESHOLD_MAP.items():
            lowerList = value["lower"].tolist()
            upperList = value["upper"].tolist()
            configFile.write(f"    '{key}': {{\n")
            configFile.write(f"        'lower': np.array({lowerList}),\n")
            configFile.write(f"        'upper': np.array({upperList})\n")
            configFile.write(f"    }},\n")
        configFile.write("}\n")
    print(f"Kaydedildi: {colorName.upper()}")

def runImageThresholdOptimizer(imagePath):
    img = cv.imread(imagePath)
    if img is None:
        print("Hata: Resim bulunamadı!")
        return

    cv.namedWindow("Settings")
    cv.resizeWindow("Settings", 640, 300)
    activeColorMode = "red"
    
    def onTrackbarChange(x): pass

    cv.createTrackbar("L-H", "Settings", 0, 179, onTrackbarChange)
    cv.createTrackbar("L-S", "Settings", 0, 255, onTrackbarChange)
    cv.createTrackbar("L-V", "Settings", 0, 255, onTrackbarChange)
    cv.createTrackbar("H-H", "Settings", 179, 179, onTrackbarChange)
    cv.createTrackbar("H-S", "Settings", 255, 255, onTrackbarChange)
    cv.createTrackbar("H-V", "Settings", 255, 255, onTrackbarChange)

    hsvFrame = cv.cvtColor(img, cv.COLOR_BGR2HSV)

    while True:
        lH = cv.getTrackbarPos("L-H", "Settings")
        lS = cv.getTrackbarPos("L-S", "Settings")
        lV = cv.getTrackbarPos("L-V", "Settings")
        hH = cv.getTrackbarPos("H-H", "Settings")
        hS = cv.getTrackbarPos("H-S", "Settings")
        hV = cv.getTrackbarPos("H-V", "Settings")

        lowerBound = np.array([lH, lS, lV])
        upperBound = np.array([hH, hS, hV])
        
        colorMask = cv.inRange(hsvFrame, lowerBound, upperBound)
        previewFrame = cv.bitwise_and(img, img, mask=colorMask)

        cv.putText(previewFrame, f"MOD: {activeColorMode.upper()}", (10, 40), 
                    cv.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2)
        
        cv.imshow("Orijinal Resim", img)
        cv.imshow("Filtrelenmis Resim", previewFrame)

        key = cv.waitKey(1) & 0xFF
        if key == ord('r'): activeColorMode = "red"
        elif key == ord('g'): activeColorMode = "green"
        elif key == ord('b'): activeColorMode = "blue"
        elif key == ord('s'): updateConfigFile(activeColorMode, lowerBound, upperBound)
        elif key == ord('q'): break

    cv.destroyAllWindows()

runImageThresholdOptimizer('v2/test-images/laptopsal.jpeg')