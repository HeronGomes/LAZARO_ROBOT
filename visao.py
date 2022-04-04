#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import cv2 as cv
import numpy as np
import time
from fala import Fala
from audicao import Audicao

camera_index = 2
rosto_cascade = 'rosto.xml'
pessoa_cascade = 'rosto.xml' #Pensar sobre isso colocar o corpo
tempo_limite = 10

modelo_treinamento = "lbph.yml"

menu_visao = """
            Módulo de visão computacional, lista de opções,
            
            Foto, captura a imagem e a renderiza,
            
            Predador, Inicia captura por visão térmica,
            
            Contagem, Realiza a contagem e reconhecimento de pessoas,
            
            Identificar, Identifica os seres humanos nas fotos,
            
            Noturno, Inicia o módulo de visão noturna,

            Para repetir, diga, MENU,
            
            Para voltar ao menu principal, diga, voltar
"""

dict_pessoa = {
        
    1:'Suelen,',
    2:'Rafael,',
    3:'Romário,',
    4:'Ronan,',
    5:'Jhonatan,',
    6:'Keller,',
    7:'Felipe,',
    8:'Filipe,',
    9:'Heron,',
    10:'Dioguinho,',
    -1:'Verificado humano não conhecido,'
}

lista_individos_reconhecidos =[]

class Visao():
       
    
    def __init__(self):
        
        self.cam = cv.VideoCapture()
        self.haarPessoa = cv.CascadeClassifier(pessoa_cascade)
        self.haarRosto = cv.CascadeClassifier(rosto_cascade)
        self.reconhecedor = cv.face.LBPHFaceRecognizer_create()
        self.reconhecedor.read(modelo_treinamento)
        self.fala = Fala()
        self.audicao = Audicao()
        
    def isParadaFuncao(self,limite,inicio):
        tempo = time.time() - inicio
        return True if (tempo < limite) else False
    
    def iniciaCamera(self):
        try:
            if self.cam.isOpened():
                self.fechaCamera()
                self.cam.open(camera_index)
            else:
                self.cam.open(camera_index)
        except Exception:
            raise Exception('Não foi possível inicir visão, verifique o dispositivo.')
    
    def fechaCamera(self):
        
        try:
            self.cam.release()
        except Exception:
            raise Exception('Não é possível finalizar o processo, reinicie o Kernel.')
    
    
    def tirarFoto(self):
        try:
            self.iniciaCamera()
            self.inicio = time.time()
            while self.isParadaFuncao(tempo_limite,self.inicio):
                isCaptura,frame = self.cam.read()
                if isCaptura:
                    cv.imshow("Imagem Capturada", frame)
                    cv.waitKey(50)
                else:
                    raise Exception("Não foi possível capturar a imagem.")
            self.fechaCamera()
            cv.destroyAllWindows()
        except Exception:
            raise Exception('Erro ao realizar comando')
        
        
    def visaoTermica(self):
        try:
            self.iniciaCamera()
            self.inicio = time.time()
            while self.isParadaFuncao(tempo_limite,self.inicio):
                isCaptura,frame = self.cam.read()
                if isCaptura:
                    #frame = cv.resize(frame, (500,500))
                    #termal_Jet = cv.applyColorMap(frame, cv.COLORMAP_JET)
                    #termal_RainBow = cv.applyColorMap(frame, cv.COLORMAP_RAINBOW)
                    termal_HSV = cv.applyColorMap(frame, cv.COLORMAP_HSV)
                    
                    #cv.imshow("Visão JET", termal_Jet)
                    #cv.imshow("Visão RAINBOW", termal_RainBow)
                    cv.imshow("Visão Térmica", termal_HSV)
                    cv.waitKey(50)
                else:
                    raise Exception("Não foi possível capturar a imagem.")
            self.fechaCamera()
            cv.destroyAllWindows()
        except Exception:
            raise Exception('Erro ao realizar comando')
            
    def detectaPessoa(self,frame):
        frame_cinza = cv.cvtColor(frame, cv.COLOR_BGR2GRAY)
        rect = self.haarPessoa.detectMultiScale(frame_cinza, scaleFactor=1.2, minNeighbors=4, minSize=(30, 30),
                                     flags=cv.CASCADE_SCALE_IMAGE)
        
        return rect if len(rect) > 0 else None
    
    def detectaRosto(self,frame):
        frame_cinza = cv.cvtColor(frame, cv.COLOR_BGR2GRAY)
        rect = self.haarRosto.detectMultiScale(frame_cinza, scaleFactor=1.2, minNeighbors=4, minSize=(30, 30),
                                     flags=cv.CASCADE_SCALE_IMAGE)
        
        return rect if len(rect) > 0 else None
    
    
    
    def desenhaROI(self,rect,frame):
        
        for x1, y1, w , h in rect:
            color = list(np.random.random(size=3) * 256)
            cv.rectangle(frame, (x1, y1), (x1+w, y1+h), color, 2)
        return frame
        
    def contarPessoa(self):
        try:
            self.iniciaCamera()
            self.inicio = time.time()
            while self.isParadaFuncao(tempo_limite,self.inicio):
                isCaptura,frame = self.cam.read()
                if isCaptura:
                    
                    self.rect = self.detectaPessoa(frame)
                    
                    if self.rect is not None:
                        frame = self.desenhaROI(self.rect, frame)
                    
                    cv.imshow("Contagem de Humanos", frame)
                    cv.waitKey(50)
                    
                else:
                    raise Exception("Não foi possível capturar a imagem.")
            if self.rect is not None:
                self.fala.falar('Indivíduos detectados , '+str(len(self.rect)))
                
            cv.destroyAllWindows()
            self.fechaCamera()
        except Exception:
                raise Exception('Erro ao realizar comando')
    
    def executarModeloPredicao(self,rect,frame):
        frame_cinza = cv.cvtColor(frame, cv.COLOR_BGR2GRAY)
        for x,y,w,h in rect:
            #cv.imshow('Detection Person',frame_cinza[y:y+h,x:x+w])
            id,conf = self.reconhecedor.predict(frame_cinza[y:y+h,x:x+w])
            lista_individos_reconhecidos.append(id)
            
    def retornarIdentificados(self):
        
       return [dict_pessoa.get(indice) for indice in set(lista_individos_reconhecidos)]
    
    def dizerResultados(self):
        
        lstResultado = self.retornarIdentificados()
        
        if not lstResultado:
        
            self.fala.falar("Nenhum, humano, identificado.")
            
        else:
            self.fala.falar("Os seguintes resultados foram encontrados:")
            self.fala.falar(lstResultado)
    
    def identificaPessoa(self):
        
        try:
            self.iniciaCamera()
            self.inicio = time.time()
            while self.isParadaFuncao(tempo_limite,self.inicio):
                isCaptura,frame = self.cam.read()
                if isCaptura:
                    
                    self.rect = self.detectaRosto(frame)
                    
                    if self.rect is not None:
                        self.executarModeloPredicao(self.rect, frame)
                        frame = self.desenhaROI(self.rect, frame)
                    
                    cv.imshow("Humanos Conhecidos", frame)
                    cv.waitKey(50)
                    
                else:
                    raise Exception("Não foi possível capturar a imagem.")
            self.dizerResultados()
            cv.destroyAllWindows()
            self.fechaCamera() 
        except Exception:
            raise Exception('Erro ao realizar comando')   
            
            
            
    
    def visaoNoturna(self):
        import os
        os.environ["OPENCV_FFMPEG_CAPTURE_OPTIONS"] = "rtsp_transport;udp" #Ajuste para o opencv
        
        
        self.camNoturna = cv.VideoCapture()
        self.camNoturna.open('rtsp://192.168.0.101:554/onvif2')
        self.inicio = time.time()

        while self.isParadaFuncao(tempo_limite,self.inicio):
            isCaptura,frame = self.camNoturna.read() 
            if isCaptura:
                frame = cv.transpose(frame) #por conta da camera invertida
                frame = cv.flip(frame,0) #por conta da camera invertida
                cv.imshow("Vião Noturna", frame)
                cv.waitKey(50)
            else:
                raise Exception("Não foi possível capturar a imagem.")
        cv.destroyAllWindows()
        self.camNoturna.release() 
        
    
        
    def start(self):
        
        try:
        
            #self.fala.falar(menu_visao)
            
            while True:
                
                comando = self.audicao.ouvir()
                
                if comando == 'FOTO':
                    self.tirarFoto()
                elif comando == 'PREDADOR':
                    self.visaoTermica()
                elif comando == 'CONTAGEM':
                    self.contarPessoa()
                elif comando == 'IDENTIFICAR':
                    self.identificaPessoa()
                elif comando == 'MENU':
                    self.fala.falar(menu_visao)
                elif comando == 'VOLTAR':
                    break
                else: 
                    pass
        except Exception as err:
            raise err
        
        