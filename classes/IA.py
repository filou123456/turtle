import torch.nn as nn
import os
import torch
from torchvision import datasets, transforms
from torch.utils.data import DataLoader
import torch.optim as optim
import cv2
import numpy as np
from torchvision import transforms
from param import *


class IA:

    def __init__(self):

        self.modele = nn.Sequential(
        nn.Conv2d(3, 16, 3, padding=1),	# nb de couleurs (3), 16 filtres donc 16 images, kernel (3x3) 
        nn.ReLU(), # fonction d’activation Rectified Linear Unit
        nn.MaxPool2d(2), # maximum sur une fenêtre 2x2, réduction spatiale de 2 
        nn.Conv2d(16, 32, 3, padding=1), # 16 images , 32 filtres 3x3 donc sortie 32 images de 
        nn.ReLU(), # fonction d’activation Rectified Linear Unit
        nn.MaxPool2d(2), # maximum sur une fenêtre 2x2, réduction spatiale de 2 
        nn.Flatten(), # passe de 2D à 1D 
        nn.Linear(32 * 32 * 32, 128), # images 32x32 (128->64->32) x32 filtres réseau de neurones standards 32768 à 128
        nn.ReLU(),  # fonction d’activation Rectified Linear Unit
        nn.Linear(128, NB_CLASSES) # réseau de neurones standards 128 à num_classes
        )
     

        self.image_transform = transforms.Compose([            # pipeline de transformation  
            transforms.Resize((TAILLE_IMG, TAILLE_IMG)),  # redimesionner l'image
            transforms.ToTensor()                         # représenter l'image à l'aide de Tensor
        ])

        # Informe Pytorch du type de donnée et de emplacement
        # Installe un pipeline de transformation
        self.entrainement_dataset = datasets.ImageFolder(os.path.join(IMAGE_DIR, "entrainement"), 
                                                    transform=self.image_transform)

        # DataLoader retourne les images par lot de TAILLE_LOT
        self.entrainement_loader = DataLoader(self.entrainement_dataset, 
                                        batch_size=TAILLE_LOT, shuffle=True)
    

    def entrainement(self): 
        # Une méthode pour entraîner le modèle à partir d’une banque d’images sur le disque. Utilisez les paramètres d'entraînement suivants :

        LEARNING_RATE = 0.001	# Taux d’apprentissage
        NUM_EPOCHS    = 60	    # Nombre d’itérations d'entraînement

        # Vérifier la présence d'un processeur graphique GPU
        self.device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

        criterion = nn.CrossEntropyLoss()	    # Fonction de coût
        optimizer = optim.Adam(self.modele.parameters(), lr=LEARNING_RATE)	# Descente de gradient kf2
        self.modele.to(self.device)
        self.modele.train()   # activer le modèle en mode entrainement
        for epoch in range(NUM_EPOCHS):  # num_epochs itération de toutes les images
            total_loss, correct = 0, 0
            for images, labels in self.entrainement_loader:
                images, labels = images.to(self.device), labels.to(self.device)
                outputs = self.modele(images)
                loss = criterion(outputs, labels)
                optimizer.zero_grad()
                loss.backward()
                optimizer.step()
                total_loss += loss.item()
                correct += (outputs.argmax(1) == labels).sum().item() # Nombre de prédictions correctes 
                                                                    # dans un batch
            acc = 100 * correct / len(self.entrainement_loader.dataset)
            print(f"Epoch {epoch+1}, Loss: {total_loss:.4f}, Accuracy: {acc:.2f}%")
    def evaluer(self):
        #Une méthode pour évaluer le modèle à l’aide d’une banque d’images sur le disque.
        self.validation_dataset = datasets.ImageFolder(os.path.join(IMAGE_DIR, "validation"), 
                                          transform=self.image_transform)
        self.validation_loader = DataLoader(self.validation_dataset, 
                                    batch_size=TAILLE_LOT, shuffle=True)
        self.modele.eval()	# activer le modèle en mode évaluation
        correct = 0
        with torch.no_grad():	# économise temps et mémoire
                                # torch.no_grad() désactive le calcule du gradiant
                                # pour le bloc d'instruction qui n'est pas nécessaire
                                # pour les prédictions du modèle
            for images, labels in self.validation_loader:
                # images: contient un lot de TAILLE_LOT image
                # labals: contient les label de toutes les images dans images
                images, labels = images.to(self.device), labels.to(self.device)
                outputs = self.modele(images)
                # outputs: contient la probabilité pour chacune des classes pour chaque image
                print(f"outputs: {outputs.shape}")

                pred_res = outputs.argmax(1) # l'index 0 / 1 de la predic. la plus grande
                performance = pred_res == labels 
                print(f"performance: {performance}")
                print(f"pred_res: {pred_res}, performance: {performance.sum().item()}")

                correct += (outputs.argmax(1) == labels).sum().item()

        acc = 100 * correct / len(self.validation_loader.dataset) 
        print(f"Accuracy: {acc:.2f}%")
    
    def presenceObstacle(self, image):
        #Une méthode qui prend une image en paramètre et qui retourne s’il y a un obstacle ou non dans l’image 
        return
        
    def sauvegarderModel(self):
        torch.save(self.modele.state_dict(), CHEMIN)
        #Une méthode pour sauvegarder le modèle sur le disque
    def chargerModel(self):
        self.modele.load_state_dict(torch.load(CHEMIN))
        # Une méthode pour charger le modèle du disque.

ia = IA()

ia.entrainement()
ia.evaluer()
ia.sauvegarderModel()