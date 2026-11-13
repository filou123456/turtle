#Params et constantes

#Paramètres image
TAILLE_LARGEUR = 480
TAILLE_HAUTEUR = 640 
ECHELLE = 100 #1m = 100 pixel
CENTRE_LARGEUR = TAILLE_LARGEUR / 2
CENTRE_HAUTEUR = TAILLE_HAUTEUR / 2

#Envoie de message
APP_CTRL_ROBOT = 8000 
APP_LIGNE = 8001
APP_PATROUILLEUR = 8002
#Les nombres indiquent les actions qui peut être transmis vers le robot
MSG_AVANCER = 1
MSG_RECULER = 2
MSG_PIVOTER_G = 3
MSG_PIVOTER_D = 4
MSG_ARRETER = 5
MSG_ACCELERER = 6
MSG_RALENTIR = 7
MSG_QUITTER = 8
MSG_POSITION = 9
MSG_INIT = 10
MSG_SONAR = 11
MSG_IMU_INFO = 12
CHANGEMENTVITESSE = 0.05 #Changement de la vitesse quand on accélère / ralentie
MAXVITESSE = 1  #Vitesse maximal
VITESSEINITIAL = 0.5 #Vitesse de départ choisit par nous

# Parametres encodeur
CIRCONFERENCE_ROUE = 21.5
TRANSITIONS_ROUE = 40


#Parametres robot
POSITION_DEPART = (0, 0) # (x, y)
L = 0.13  # distance entre les deux roues (13cm)

#Autres
VITESSE_SON = 343 #m/s

#Paramètre camra/HSV
SURFACE_MIN = 150 
SURFACE_MAX = 7000 
LARGEUR = 320
HAUTEUR = 240

#Paramètre IMU
G = 9.80665
INTERVALLE_IMU = 0.05 # 50ms 


#scp -r "C:\Users\maxim\Documents\environnement\labo4\classes" pi@192.168.137.135:/home/pi/

#Tranfer
#source ~/pyenv/bin/activate
#scp -r "C:\Users\maxim\Documents\GitHub\turtle\classes" pi@192.168.137.32:/home/pi/