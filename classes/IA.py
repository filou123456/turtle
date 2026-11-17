import torch.nn as nn
import os
import torch
from torchvision import datasets, transforms
from torch.utils.data import DataLoader
import torch.optim as optim
import cv2
import numpy as np
from torchvision import transforms

NB_CLASSES = 2
modele = nn.Sequential(
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

IMAGE_DIR = "./image_rgb/" 

TAILLE_LOT = 32  
TAILLE_IMG = 128

image_transform = transforms.Compose([            # pipeline de transformation  
    transforms.Resize((TAILLE_IMG, TAILLE_IMG)),  # redimesionner l'image
    transforms.ToTensor()                         # représenter l'image à l'aide de Tensor
])

# Informe Pytorch du type de donnée et de emplacement
# Installe un pipeline de transformation
entrainement_dataset = datasets.ImageFolder(os.path.join(IMAGE_DIR, "entrainement"), 
                                            transform=image_transform)

# DataLoader retourne les images par lot de TAILLE_LOT
entrainement_loader = DataLoader(entrainement_dataset, 
                                 batch_size=TAILLE_LOT, shuffle=True)

print("dataset info")
print(f"Classes: {entrainement_dataset.classes}")
print(f"Images par classe: {entrainement_dataset.targets.count(0)}, {entrainement_dataset.targets.count(1)}")
print(f"Nombre d'images:",len(entrainement_dataset))
print(f"Premiere image: {entrainement_dataset.samples[0]}")

print("loader info:")
imgs, targets = next(iter(entrainement_loader)) # retourne les images par lot de TAILLE_LOT
print(f"nombre de lots: {len(entrainement_loader)}")
print(f"nombre de lots: {len(entrainement_loader.dataset)}")

print(f"Image data type: {type(imgs)}")
print(f"Image batch size: {imgs.shape}")  # dimensions are (batch size, image channels, image height, image width)
print(f"Target batch size: {targets.shape}")

LEARNING_RATE = 0.001	# Taux d’apprentissage
NUM_EPOCHS    = 10	    # Nombre d’itérations d'entraînement

# Vérifier la présence d'un processeur graphique GPU
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

criterion = nn.CrossEntropyLoss()	    # Fonction de coût
optimizer = optim.Adam(modele.parameters(), lr=LEARNING_RATE)	# Descente de gradient kf2
modele.to(device)
modele.train()   # activer le modèle en mode entrainement
for epoch in range(NUM_EPOCHS):  # num_epochs itération de toutes les images
	total_loss, correct = 0, 0
	for images, labels in entrainement_loader:
		images, labels = images.to(device), labels.to(device)
		outputs = modele(images)
		loss = criterion(outputs, labels)
		optimizer.zero_grad()
		loss.backward()
		optimizer.step()
		total_loss += loss.item()
		correct += (outputs.argmax(1) == labels).sum().item() # Nombre de prédictions correctes 
															  # dans un batch
	acc = 100 * correct / len(entrainement_loader.dataset)
	print(f"Epoch {epoch+1}, Loss: {total_loss:.4f}, Accuracy: {acc:.2f}%")
 
validation_dataset = datasets.ImageFolder(os.path.join(IMAGE_DIR, "validation"), 
                                          transform=image_transform)
validation_loader = DataLoader(validation_dataset, 
                               batch_size=TAILLE_LOT, shuffle=True)

modele.eval()	# activer le modèle en mode évaluation
correct = 0
with torch.no_grad():	# économise temps et mémoire
                        # torch.no_grad() désactive le calcule du gradiant
                        # pour le bloc d'instruction qui n'est pas nécessaire
                        # pour les prédictions du modèle
    for images, labels in validation_loader:
        # images: contient un lot de TAILLE_LOT image
        # labals: contient les label de toutes les images dans images
        images, labels = images.to(device), labels.to(device)
        outputs = modele(images)
        # outputs: contient la probabilité pour chacune des classes pour chaque image
        print(f"outputs: {outputs.shape}")

        pred_res = outputs.argmax(1) # l'index 0 / 1 de la predic. la plus grande
        performance = pred_res == labels 
        print(f"performance: {performance}")
        print(f"pred_res: {pred_res}, performance: {performance.sum().item()}")

        correct += (outputs.argmax(1) == labels).sum().item()

acc = 100 * correct / len(validation_loader.dataset) 
print(f"Accuracy: {acc:.2f}%")

CHEMIN = "./pt_modele/kf2_modele.pt"

# Sauvegarder uniquement les paramètres: 
torch.save(modele.state_dict(), CHEMIN)

# Charger uniquement les paramètres: 
modele.load_state_dict(torch.load(CHEMIN))

import matplotlib.pyplot as plt

image = plt.imread("image_rgb/validation/continuer/image_122.png")
print(image.shape)
plt.imshow(image, cmap='gray')
plt.axis('off')
labels =  ['arreter', 'continuer']  # en ordre alphabétique
    
# Prétraitement de l’image

image = cv2.resize(image, (TAILLE_IMG, TAILLE_IMG))

# image = cv2.cvtColor(frame_resized, cv2.COLOR_BGR2RGB) # Peut-être pas nécessaire
   
# Permutation des axes Hauteur, Largeur, Canal en CHL 
# Unsqueeze ajoute une dimension pour le numéro du batch (batch, C, H, L)
# Diviser par 255 pour nomaliser les valeurs des couleur BGR
image_tensor = torch.tensor(image.transpose(2, 0, 1)).float().unsqueeze(0) / 255.0

image_tensor = image_tensor.to(device)

with torch.no_grad():
    output = modele(image_tensor)
    _, predicted = torch.max(output, 1) # max de la dimension 1
label = labels[predicted.item()] if predicted.item() < len(labels) else "?"
print(output, label)