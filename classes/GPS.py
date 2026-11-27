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

        #DÃ©marrer la communication avec la borne
        self.ser.write(b'\r\r')
        time.sleep(1)
        self.ser.write(b'lep\n')

    def getPos(self):
        #avoir la position devrait etre dans une loop pour constament avoir le data

        data = self.ser.readline().decode('utf-8').strip()  # data meow
        #Regarder si les 3 premières lettres sont POS sinon on return 0,0,0,0 (qui devrait être ignorer)
        if data[:3] == "POS":

                dataSplit = data.split(',')
                x = dataSplit[1]
                y = dataSplit[2]
                z = dataSplit[3]
                qualite = dataSplit[4]
                return (x,y,z,qualite)
        return (0,0,0,0)

    def closeGPS(self):
        self.ser.close()

        
gps = GPS()
while True:

    (x,y,z,qualite) = gps.getPos()
    if ((x,y,z,qualite) != (0,0,0,0)): #Ignore (0,0,0,0)
        print(x,y,z,qualite)

    

