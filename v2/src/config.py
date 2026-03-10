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
IMAGE_IN = os.path.join(TEST_IMAGES_DIR, "mavi1.jpeg")
IMAGE_OUT = os.path.join(TEST_IMAGES_DIR, "sonuc_kusbakisi.png")

REAL_WIDTH = 30.41
REAL_HEIGHT = 21.50
SCALE = 30

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