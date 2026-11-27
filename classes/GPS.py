from param import *
import serial
import time
class GPS :
    def __init__(self):
        self.ser = serial.Serial()
        self.ser.port = "/dev/ttyACM0"
        self.ser.baudrate = 115200
        self.ser.bytesize = serial.EIGHTBITS
        self.ser.parity = serial.PARITY_NONE
        self.ser.stopbits = serial.STOPBITS_ONE
        self.ser.timeout = 1
        self.ser.open()
        self.ser.write(b'\r\r')
        time.sleep(1)
    def getPos(self):
        #avoir la position devrait être dans une loop pour constament avoir le data
        self.ser.write(b'lep\n')
        data = str(self.ser.readline())
        print(data)
        dataSplit = data.split(',')
        if (dataSplit[0] == 'POS'):
            dataSplit.remove('POS')
        (x,y,z,angle) = dataSplit
        return (x,y,z,angle)

    def closeGPS(self):
        self.ser.close()
        

gps = GPS()
while True:
    (x,y,z,angle) = gps.getPos()
    print(x,y,z,angle);
    
