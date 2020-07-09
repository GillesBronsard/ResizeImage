# -*-coding:Latin-1 -*

"""
Prerequis : installer pillow (fork de PIL) :
py - m pip install pillow

Nom du projet : ResizeImage

Date de la derniere revision : 08-07-2020

Auteur : Gilles BRONSARD

Révision N° : Version 1.2

Client : 

Fichiers du projet :
                    -    main.py
                    -    Chemins.txt
                    -    log.log

"""

from PIL import Image
from os import listdir
from os.path import isfile, isdir, join, basename
import glob
import time
import os
import warnings

#-------------------------------------------------------
#        Zone de déclaration des fonctions
#-------------------------------------------------------

#Retourne la largeur d'un fichier
def whatWidth (source):
    try:
        maPic = Image.open(source)
        if maPic.size[0] > 8000: 
            pass
        else: 
            return(maPic.size[0])
    except IOError:
        pass
#Test    
#print(whatWidth("c:/temp/portrait.jpg"))

#-------------------------------------------------------    
#Retourne la hauteur d'un fichier
def whatHeight(source):
    try:  
        maPic = Image.open(source)
        if maPic.size[0] > 8000:
            pass
        else:
            return(maPic.size[1])
    except IOError:
        pass
#Test    
#print(whatHeight("c:/temp/portrait.jpg"))  

#-------------------------------------------------------   
#Redimensionner des images en JPG et BMP dans un dossier unique

def resizImage(source, diMax):
    imageFiles = [ f for f in listdir(source) if isfile(join(source,f)) and (f.endswith("JPG") or f.endswith("jpg")) ] #or f.endswith("BMP") or f.endswith("bmp")) ]
    target = int(diMax)
    for im in imageFiles :
        if whatWidth(source+"/"+im)==None or whatWidth(source+"/"+im)==2048 or whatHeight(source+"/"+im)==2048 or whatWidth(source+"/"+im)<2048 and whatHeight(source+"/"+im)<2048:
            pass
        else:
            try:
                im1 = Image.open(join(source,im))
                originalWidth, originalHeight = im1.size
                ratio = originalWidth / originalHeight
                if ratio > 1 :
                    width = target
                    height = int(width / ratio)
                else :
                    height = target
                    width = int(height * ratio)
                im2 = im1.resize((width, height), Image.ANTIALIAS)
                #im2.save(join(source, "".join([str(width),"x",str(height),"_",im]))) #Permet de ne pas ecraser l'original
                im2.save(source+'/'+im)
            except (IOError, FileNotFoundError):#Erreur sur les photos panoramiques et fichiers non trouvés
                pass
    try:
        with open("C:/PY/ResizeImageFinal/log.log", "a") as fic:
            dossier = source + " : Dossier traité le {}".format(time.strftime("%d/%m/%Y à %H:%M"))
            fic.write("\n"+ str(dossier))
    except UnboundLocalError:
        print("Le dossier", source, "est vide")

#Test
#resizImage("C:/temp/Dossier01/Bureaux Nantes", 2048)

#______________________________________________________________    
#Remplace les \ par des /
def reverseSlash(chaine):
    var2 = 0
    backSla = ['\\', '\t', '\n']
    slashi = ['/', '/t', '/n']
    for var2 in range(3):
        chaine = chaine.replace(backSla[var2], slashi[var2])
        var2 +=1
    return(chaine)
#Test
#print(reverseSlash("C:\temp\Dossier01\Dossier 01 02"))		

#______________________________________________________________ 
#Retourne une arborescence de dossiers contenant le mot Photo et applique resizImage, exclut les dossiers intitulé HD, hd et comportant le mot plan ou Plan

def allChemRecurs(Chemin) :
    dossiers = glob.glob(os.path.join(Chemin, "**"), recursive=True)
    for dossier in dossiers:
        if isdir(dossier):
            if "Photo" or "photo" in dossier:
                if basename(dossier)=="HD" or basename(dossier)=="hd" or "plan" in dossier or "Plan" in dossier:
                    pass
                else:                 
                    try:
                        chemUnParUn = reverseSlash(dossier)
                        resizImage(chemUnParUn, 2048)
                    except (UnicodeEncodeError, FileNotFoundError, PermissionError):
                        pass
    return('')   
#Test
#allChemRecurs("//SRV-FICHIERS/datas/AFFAIRES BETREC/18357 - ROMPON (07) -CONST 7 A 9 LOGTS + AMENAGT")

#--------------------------------------------------------------------------------------------------------------
#        Programme
#--------------------------------------------------------------------------------------------------------------

#Desactive la limite de taille de fichier max pour eviter les DecompressionBombWarning
Image.MAX_IMAGE_PIXELS = None 

with open('log.log', "w") as fic:
    fic.write('Dossiers traités:')

Le fichier Chemins.txt contient les emplacements à traiter (fichier modifiable)
listeAtraiter = []
with open('Chemins.txt') as f :
    for line in f :
        listeAtraiter.append(line)

for cheminn in listeAtraiter:
    allChemRecurs(cheminn.strip())
