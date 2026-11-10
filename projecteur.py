import math
from params import *
import numpy as np
class Projecteur:
    def __init__(self):
        self.points = [] #tableau de tuple de coords x,y
        self.pointsImage = []

        
#recois distance et angle A
    def calculerCordPolaire(self,angle,range):
        x = -range*math.sin(angle)
        y = range*math.cos(angle)
        self.points.append((x,y))
        return (x,y) #Si on a besoin d'avoir les coords
    def mettreAEchelle(self):
        for x,y in self.points:
            xImage = CENTRE_LARGEUR + x * ECHELLE
            yImage = CENTRE_HAUTEUR + y * ECHELLE
            self.pointsImage((xImage,yImage))
    def projeter(self,tabVecteur):#
        for range,angle in tabVecteur:
            self.calculerCordPolaire(angle,range)
        self.mettreAEchelle()
        
        image = np.zeros((TAILLE_LARGEUR,TAILLE_HAUTEUR,3),np.uint8)
            
    
    
        
