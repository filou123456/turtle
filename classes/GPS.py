from param import *
import serial
import time
class GPS :
    def __init__(self):


        #Obtenir la position du robot 
        self.ser = serial.Serial()
        self.ser.port = "/dev/ttyACM0"
        self.ser.baudrate = 115200
        self.ser.bytesize = serial.EIGHTBITS
        self.ser.parity = serial.PARITY_NONE
        self.ser.stopbits = serial.STOPBITS_ONE
        self.ser.timeout = 1
        self.ser.open()

        #Démarrer la communication avec la borne
        self.ser.write(b'\r\r')
        time.sleep(1)

    def getPos(self):
        #avoir la position devrait être dans une loop pour constament avoir le data
        self.ser.write(b'lep\n')
        data = str(self.ser.readline())  # data meow
        print(data)
        dataSplit = data.split(',')

        if (dataSplit[0] == 'POS'):
            dataSplit.remove('POS')
        (x,y,z,qualite) = dataSplit

        return (x,y,z,qualite)

    def closeGPS(self):
        self.ser.close()
        

gps = GPS()

while True:
    (x,y,z,qualite) = gps.getPos()
    print(x,y,z,qualite)
    
