import os
from PIL import Image
import cv2
import subprocess
from moviepy.video.io.ffmpeg_tools import ffmpeg_extract_subclip
from moviepy.video.io.VideoFileClip import VideoFileClip


dossier_sortie = "images"  # Dossier de sortie pour enregistrer les images
dossier_sortie_img_r = "imaages_r"
os.makedirs(dossier_sortie_img_r, exist_ok=True)
os.makedirs(dossier_sortie, exist_ok=True)

def clear_files(dossier):
    # Supprimer tous les fichiers dans le dossier spécifié
    for filename in os.listdir(dossier):
        file_path = os.path.join(dossier, filename)
        os.remove(file_path)

    # Supprimer le dossier lui-même
    os.rmdir(dossier)
    

# Supprimer les fichiers générés
clear_files(dossier_sortie)
clear_files(dossier_sortie_img_r)

def decouper_video(debut, fin, intervalle, dossier_sortie):
    # Convertir l'intervalle en un nombre entier de millisecondes
    intervalle_ms = int(intervalle * 1000)

    # Couper la vidéo à l'aide de MoviePy
    video = VideoFileClip("bad_appel.mp4").subclip(debut, fin)

    # Créer un dossier pour enregistrer les images extraites
    os.makedirs(dossier_sortie, exist_ok=True)

    # Extraire des images de la vidéo selon l'intervalle spécifié
    i = 1
    for t in range(0, int(video.duration * 1000), intervalle_ms):
        image = video.get_frame(t / 1000)  # Convertir le temps en secondes
        image_path = os.path.join(dossier_sortie, "{i}.jpg")
        cv2.imwrite(image_path, cv2.cvtColor(image, cv2.COLOR_RGB2BGR))
        i += 1

    # Fermer la vidéo
    video.reader.close()

    print("Extraction des images terminée.")


def resize_images(input_folder, output_folder, width, height):
    # Vérifier si le dossier de sortie existe, sinon le créer
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    # Parcourir tous les fichiers dans le dossier d'entrée
    for filename in os.listdir(input_folder):
        # Vérifier si le fichier est une image
        if filename.endswith(('.jpg', '.jpeg', '.png', '.gif')):
            # Charger l'image
            image_path = os.path.join(input_folder, filename)
            image = Image.open(image_path)

            # Redimensionner l'image avec la dimension précise
            resized_image = image.resize((width, height))

            # Enregistrer l'image redimensionnée dans le dossier de sortie
            output_path = os.path.join(output_folder, filename)
            resized_image.save(output_path)

            print(f"Image {filename} redimensionnée avec succès.")

def clear_console():
    os.system('cls' if os.name == 'nt' else 'clear')
    print('\n' * 100)

def decouper_image_en_pixels(image_path):
    image = Image.open(image_path).convert("1")
    largeur, hauteur = image.size
    pixels = image.load()

    tableau_pixels = []
    for y in range(hauteur):
        ligne_pixels = ""
        for x in range(largeur):
            if pixels[x, y] == 0:
                ligne_pixels += "."
            else:
                ligne_pixels += " "
        tableau_pixels.append(ligne_pixels)

    return tableau_pixels

def afficher_pixels(image_pixels):
    largeur_image = len(image_pixels[0])

    cadre = "+" + "-" * largeur_image + "+"
    print(cadre)
    for ligne in image_pixels:
        print("|" + ligne + "|")
    print(cadre)

def traiter_dossier_images(dossier_path):
    images = [f for f in os.listdir(dossier_path) if os.path.isfile(os.path.join(dossier_path, f))]
    tableau_pixels = []

    for image_file in images:
        image_path = os.path.join(dossier_path, image_file)
        pixels_image = decouper_image_en_pixels(image_path)

        afficher_pixels(pixels_image)

        tableau_pixels.extend(pixels_image)

        clear_console()
        tableau_pixels.clear()
        

debut = 0  # Temps de début de la vidéo en secondes
fin = 219  # Temps de fin de la vidéo en secondes
intervalle = 0.006944444444  # Intervalle de temps entre chaque image en secondes

decouper_video(debut, fin, intervalle, dossier_sortie)
resize_images(dossier_sortie, dossier_sortie_img_r, 100, 100)
traiter_dossier_images(dossier_sortie_img_r)

