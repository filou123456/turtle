import math
from params import *
import numpy as np
import cv2
class Projecteur:
         
#recois distance et angle A
    def calculerCordPolaire(self,angle,range):
        x = -range*math.sin(angle)
        y = range*math.cos(angle)

        return (x,y)

    def mettreAEchelle(self,x,y):
        xImage = CENTRE_LARGEUR + x * ECHELLE
        yImage = CENTRE_HAUTEUR + y * ECHELLE
        return (int(xImage),int(yImage))
                     
    def projeter(self,tabVecteur):
        image = np.zeros((TAILLE_HAUTEUR, TAILLE_LARGEUR, 3),np.uint8)
        for range,angle in tabVecteur:
            x,y = self.calculerCordPolaire(angle,range) 
            xImage,yImage = self.mettreAEchelle(x,y)    
            if (range < 0.50 and range > 0.10 and abs(math.degrees(angle)) > 10):
                cv2.circle(image, (xImage,yImage), 5, (0, 0, 255), -1)
            else:
                cv2.circle(image, (xImage,yImage), 5, (0, 255, 0), -1)
                
        cv2.imshow("Scan robot lidar", image)
        cv2.waitKey(1)
        
        
