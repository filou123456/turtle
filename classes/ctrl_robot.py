#Laboratoire 1
#Fait par : Maxime Tremblay Félix-Antoine Montreuil
#1 septembre 2026
#Initialisation du robot et contrôle de celui-ci
from ev_app import *
from param import *
import threading
from moteur import Moteur
from robot import Robot
import time
import math
from IMU import IMU
from ev_app_client_api import gen_ev_externe
from param import *

from camera import Camera

class CtrlRobot(EvApp):
    moteurGauche = Moteur(6,5,13)
    moteurDroite = Moteur(15,14,18)
    vitesse = VITESSEINITIAL
    TMO = INTERVALLE_IMU

    robot = Robot(moteurGauche, moteurDroite,VITESSEINITIAL) #Envoie la vitesse initital

    def __init__(self, port_no):
        super().__init__(port_no,tmo=CtrlRobot.TMO)
        self.imu = IMU()
        self.est_actif = False
        self.dernier_echantillonnage = time.monotonic()


    def dispatch_event(self, ev):
        # Ici on traite les messages reçus
            currentTime = time.monotonic() # current time on the counter
            dt = currentTime - self.dernier_echantillonnage # 
            print(f"message recu: {ev}")

            if (ev.type != 0 and ev.type != MSG_INIT):
                donnee = ev.split()
                vitesse = float(donnee[0])

            if ev.type == MSG_AVANCER:
                print(f"avancer robot :")
                self.robot.avancer(vitesse)
                angle_rot, dist_y = self.imu.obtenir_deplacement(True, dt)


            elif ev.type == MSG_PIVOTER_G:
                print(f"pivot g robot :")
                self.robot.tourner_gauche(vitesse)

            elif ev.type == MSG_PIVOTER_D:
                print(f"pivot d robot :")
                self.robot.tourner_droite(vitesse)
                angle_rot, dist_y = self.imu.obtenir_deplacement(True, dt)


            elif ev.type == MSG_ARRETER:
                print(f"arret robot :")
                self.robot.arreter()
                angle_rot, dist_y = self.imu.obtenir_deplacement(False, dt)

            elif ev.type == MSG_QUITTER:
                print("quitter")
                self.quitter()
            elif ev.type == MSG_INIT:
                self.robot.arreter()  
                self.robot.reset()  

       


    def quitter(self):
        # Ici on fait du ménage avant de quitter
        # si nécessaire
        print("Bye bye")
        self.robot.arreter()
        
ctrl_robot = CtrlRobot(port_no=APP_CTRL_ROBOT)
ctrl_robot.run()