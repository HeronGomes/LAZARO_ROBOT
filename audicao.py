#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import speech_recognition as sr
import re

class Audicao():
    
    def __init__(self):
        self.r = sr.Recognizer()
        self.mic = sr.Microphone() #USBGX1XK

    def ouvir(self):
        try:
            with self.mic as source:
                audio = self.r.listen(source,timeout=5)
                retorno = self.r.recognize_google(audio,language="pt-BR")
                print(retorno.upper())
                return retorno.upper()
        except Exception:  
            return None
        

    def evocacao(self):
        try:
            retorno = re.search('LÁZARO',self.ouvir())
            return retorno is not None
        except:
            return False
        