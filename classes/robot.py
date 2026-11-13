#Maxime Tremblay et Felix-Antoine Montreuil 
#Labo 1, 1er septembre 2026
#Classe Robot


from moteur import Moteur
from param import *

import math



class Robot:

    # Créer objet robot avec le moteur
    def __init__(self, moteurGauche, moteurDroite, vitesse):
        self.__moteurGauche = moteurGauche
        self.__moteurDroite = moteurDroite
        self.vitesse = vitesse
   


    #Méthodes de déplacement du robot, utilise les contrôles des noteurs 
    def tourner_gauche(self,vitesse):
            self.__moteurDroite.tourner(vitesse)
            self.__moteurGauche.reculer(vitesse) 
            

    def tourner_droite(self,vitesse):
         self.__moteurGauche.tourner(vitesse)
         self.__moteurDroite.reculer(vitesse)

    def avancer(self,vitesse):
        self.__moteurDroite.avancer(vitesse)
        self.__moteurGauche.avancer(vitesse)

        

    def reculer(self,vitesse):
        self.__moteurGauche.reculer(vitesse)
        self.__moteurDroite.reculer(vitesse)

    def arreter(self):
        self.__moteurDroite.arret()
        self.__moteurGauche.arret()


        
    

    
         