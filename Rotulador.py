# -*- coding: utf-8 -*-
"""
Created on Sun Sep  8 15:02:08 2019

@author: Heron
"""

import os
import cv2
import numpy as np
import csv
from numpy.core.numeric import array



def carregaTreino(pathCSV):
    faces = []
    labels = []
    with open(pathCSV,'r',encoding='UTF-8') as csvFile:
        reader = csv.DictReader(csvFile,delimiter=';')
        for row in reader: 
            img = cv2.resize(cv2.imread(str(row['PATH']),cv2.IMREAD_GRAYSCALE),(200,200))
            if img is not None :
                faces.append(img)
                labels.append(int(row['RA']))
        return array(labels),faces
    
def executaTeste(pathCSV,treinador):
    with open(pathCSV,'r',encoding='UTF-8') as csvFile:
        reader = csv.DictReader(csvFile,delimiter=';')
        for row in reader: 
            img = cv2.resize(cv2.imread(str(row['PATH']),cv2.IMREAD_GRAYSCALE),(200,200))
            if img is not None :
               id,conf=treinador.predict(img)
               print(str(row['RA']), str(id), str(row['RA']) != str(id) , str(conf))
               if(str(row['RA']) != str(id)):
                   print("Esperado:"+str(row['RA'])+"   Predito:"+str(id)+"   Confiança:"+str(conf)) 

labels, faces = carregaTreino(r"D:\ROBOT\resultado\alunos.csv")
lbph = cv2.face.LBPHFaceRecognizer_create(10,8,5,5,50)
lbph.train(faces, np.array(labels))
lbph.save(r"D:\ROBOT\resultado\lbph.yml")



#executaTeste(r"D:\ROBOT\resultado\teste.csv",lbph)