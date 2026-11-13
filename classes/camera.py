from param import *
import cv2
import platform

class Camera: 
    
    def __init__(self, largeur, hauteur):

        self.platforme = "rien"
        self.largeur = largeur
        self.hauteur = hauteur
    
        if platform.system() == "Linux":
            from picamera2 import Picamera2
            self.Picamera2 = Picamera2
            self.platforme = "linux"

        elif platform.system() == "Windows":
            
            self.cv2 = cv2
            self.platforme = "windows"


    def demarrer(self):

        if self.platforme == "linux":

            self.picam2 = self.Picamera2()
            config = self.picam2.create_video_configuration( main={"format": "RGB888", "size": (self.largeur, self.hauteur)})

            self.picam2.configure(config)
            self.picam2.start()

        elif self.platforme == "windows":

            self.vcap = self.cv2.VideoCapture(0)
            self.vcap.set(self.cv2.CAP_PROP_FRAME_WIDTH, self.largeur)
            self.vcap.set(self.cv2.CAP_PROP_FRAME_HEIGHT, self.hauteur)

    def arreter(self):

        if self.platforme == "linux":

            self.picam2.stop()

        elif self.platforme == "windows":

            self.vcap.release()
    def capturer(self):

        if self.platforme == "linux":
            image = self.picam2.capture_array()
            image = cv2.cvtColor(image, self.cv2.COLOR_RGB2BGR)

        elif self.platforme == "windows":
            ret, image = self.vcap.read()

        return image
        