#Maxime Tremblay et Felix-Antoine Montreuil 
#Labo 1, 1er septembre 2026
#Classe moteur


import time
from param import *
from gpiozero import DigitalOutputDevice
from gpiozero import PWMOutputDevice

class Moteur:
    def __init__(self,pinIn1,pinIn2,pinEn):
        self.in1 = DigitalOutputDevice(pinIn1)
        self.in2 = DigitalOutputDevice(pinIn2)
        self.en = PWMOutputDevice(pinEn)
        self.en.value = 0

    def avancer(self, vitesse):
        self.in1.on()
        self.in2.off()
        self.en.value = vitesse

    def tourner(self, vitesse):
        self.in1.on()
        self.in2.off()
        self.en.value = vitesse

    def arret(self):
        self.in1.off()
        self.in2.off()
        self.en.off()
        self.en.value = 0

    def reculer(self,vitesse):
        self.in1.off()
        self.in2.on()
        self.en.value = vitesse