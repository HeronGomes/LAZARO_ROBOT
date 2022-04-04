# -*- coding: utf-8 -*-
"""
Created on Mon Sep  9 22:24:09 2019

@author: Heron
"""

# -*- coding: utf-8 -*-
"""
Created on Fri Oct  5 22:28:57 2018

@author: htfgh
"""
import os
import csv
import pandas as pd
from sklearn.model_selection import train_test_split

rawData ={}
RA= []
PATH = []

imagePaths=[os.path.join(r"D:\ROBOT\Treino",f) for f in os.listdir(r"D:\ROBOT\Treino")] 
for imagePath in imagePaths: 
    filePaths=[os.path.join(imagePath,f) for f in os.listdir(imagePath)] 
    for filePath in filePaths:
        RA.append((filePath.split("\\")[3]))
        PATH.append(str(filePath))

rawData = {'RA' : RA, 'PATH' : PATH}
df = pd.DataFrame(rawData, columns = ['RA', 'PATH'])
df.to_csv(r'D:\ROBOT\resultado\alunos.csv',sep=';',index = False,encoding='utf-8')


csv = pd.read_csv(r'D:\ROBOT\resultado\alunos.csv')


train , teste = train_test_split(csv , test_size=0.3 )

df = pd.DataFrame(train)
df.to_csv(r'D:\ROBOT\resultado\treino.csv',index= False,encoding='utf-8')

df = pd.DataFrame(teste)
df.to_csv(r'D:\ROBOT\resultado\teste.csv',index= False,encoding='utf-8')
