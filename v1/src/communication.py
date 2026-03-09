import time
import serial 
from config import ARDUINO_SERIAL_PORT, ARDUINO_BAUDRATE

arduinoConnection = None

def initArduino():

    global arduinoConnection

    try:
        arduinoConnection = serial.Serial(port=ARDUINO_SERIAL_PORT, 
                                          baudrate=ARDUINO_BAUDRATE, 
                                          timeout=0.1)
        
        time.sleep(2)
        print("successfully connected Arduino!")

        return True
    except:
        print("communication error!")
        return False
    

def sendToArduino(colour):
    global arduinoConnection

    if arduinoConnection and arduinoConnection.is_open:
        payload = f"{colour}\n"
        arduinoConnection.write(payload.encode('utf-8'))
        return True
    return False

def isReady():
    if arduinoConnection and arduinoConnection.in_waiting > 0:
        line = arduinoConnection.readline().decode('utf-8').strip()
        print("arduino is ready!")
        return line == "OK"
    return False

def closeArduino():
    global arduinoConnection

    if arduinoConnection:
        arduinoConnection.close()
    