import numpy as np

CAMERA_INDEX = 0
ARDUINO_SERIAL_PORT = "/dev/cu.usbmodem1101" 
BAUD_RATE_SPEED = 9600

COLOR_THRESHOLD_MAP = {
    "red": {"lower": np.array([0, 150, 50]), "upper": np.array([10, 255, 255])},
    "green": {"lower": np.array([35, 100, 50]), "upper": np.array([85, 255, 255])},
    "blue": {"lower": np.array([100, 150, 50]), "upper": np.array([140, 255, 255])}
}