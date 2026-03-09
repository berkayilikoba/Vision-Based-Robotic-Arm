import numpy as np
import os 

CAMERA_INDEX = 0
ARDUINO_SERIAL_PORT = '/dev/cu.usbmodem1101'
ARDUINO_BAUDRATE = 9600
MIN_DETECTION_AREA = 5000
STABLE_THRESHOLD = 50
REQUIRED_STABLE_TIME = 3.0 
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
TEST_IMAGES_DIR = os.path.join(BASE_DIR, "test-images")


COLOR_THRESHOLD_MAP = {
    'red': {
        'lower': np.array([0, 150, 100]),
        'upper': np.array([15, 255, 255])
    },
    'green': {
        'lower': np.array([35, 100, 50]),
        'upper': np.array([85, 255, 255])
    },
    'blue': {
        'lower': np.array([90, 110, 100]), 
        'upper': np.array([130, 255, 255])
    },
}