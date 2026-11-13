#Maxime Tremblay et Felix-Antoine Montreuil 
#Labo 1, 1er septembre 2026
#Programme qui envoie les messages au client (robot)


import sys
import numpy as np
import cv2
from param import *
import threading
from ev_app_client_api import *
img = np.zeros((512,512,3),np.uint8)
cv2.imshow('Labo 2',img)

stop_event = threading.Event()
action = 0
message = ""
vitesse = VITESSEINITIAL
while not stop_event.is_set():
    key = cv2.waitKeyEx(0) # 0: bloque l'exécution
    
        
        
    #Commandes possibles
    if key==ord('q'):
        message = "Avancer"
        action = MSG_AVANCER
        

    if key==ord('s'):
        message = "Tourner à droite"
        action = MSG_PIVOTER_D

    if key==ord('w'):
        message = "Tourner à gauche"
        action = MSG_PIVOTER_G

    if key==ord('e'):
        message = "Reculer"
        action = MSG_RECULER
    if key==ord('p'):
        message = "Capture"
        action = MSG_CAPTURER

    if key==ord('.'):
        message = "Accélération"
        if (vitesse + CHANGEMENTVITESSE > MAXVITESSE):
            vitesse = MAXVITESSE
        else:
            vitesse += CHANGEMENTVITESSE

    if key==ord(','):
        message = "Décélaration"
        if (vitesse - CHANGEMENTVITESSE < 0):
            vitesse = 0
        else :
            vitesse -= CHANGEMENTVITESSE

    if key==ord(' '):
        message = "Arrêt"
        action = MSG_ARRETER

    if key==ord('x'):
        message = "Fermeture"
        action = MSG_QUITTER
        cv2.destroyAllWindows()
        stop_event.set()
        print(f"Voilà")
    if (action != 0):
        print(f"{message}")
        gen_ev_externe(IP, APP_CTRL_ROBOT, action, vitesse)