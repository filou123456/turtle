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
from datetime import datetime
import math
import cv2
from ev_app_client_api import gen_ev_externe
from param import *

from camera import Camera


class CtrlRobot(EvApp):
    moteurGauche = Moteur(6,5,13)
    moteurDroite = Moteur(15,14,18)
    vitesse = VITESSEINITIAL
    camera = Camera(640,480)
    robot = Robot(moteurGauche, moteurDroite,VITESSEINITIAL) #Envoie la vitesse initital



    def __init__(self, port_no):
        super().__init__(port_no)


       
     


    def dispatch_event(self, ev):
        # Ici on traite les messages reçus
   
            print(f"message recu: {ev}")

            if (ev.type != 0 and ev.type != MSG_INIT):
                donnee = ev.split()
                vitesse = float(donnee[0])

            if ev.type == MSG_AVANCER:
                print(f"avancer robot :")

                self.robot.avancer(vitesse)
                     


            elif ev.type == MSG_RECULER:

                print(f"Reculer")
                self.robot.reculer(vitesse)
                


            elif ev.type == MSG_PIVOTER_G:
                print(f"pivot g robot :")
                self.robot.tourner_gauche(vitesse)
                

            elif ev.type == MSG_PIVOTER_D:
                print(f"pivot d robot :")
                self.robot.tourner_droite(vitesse)
              

            elif ev.type == MSG_ARRETER:
                print(f"arret robot :")
                self.robot.arreter()
                
           
            # elif ev.type == MSG_CAPTURER:
            #         image = self.camera.capturer()
            #         nom = datetime.now().strftime("%Y%m%d_%H%M%S") #Enregistrer avec la date pour ne pas écraser les photos
            #         cv2.imwrite(f"/home/pi/image_rgb/entrainement/{nom}.png", image)
                        
                

            elif ev.type == MSG_QUITTER:
                print("quitter")
                self.quitter()
                self.camera.arreter()
            elif ev.type == MSG_INIT:
                self.robot.arreter()  
  
            
    def quitter(self):
        # Ici on fait du ménage avant de quitter
        # si nécessaire
        print("Bye bye")
        self.robot.arreter()
        
ctrl_robot = CtrlRobot(port_no=APP_CTRL_ROBOT)
ctrl_robot.run()