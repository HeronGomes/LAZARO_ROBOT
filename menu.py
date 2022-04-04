#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from audicao import Audicao
from fala import Fala
# from matematica import Matematica
# from visao import Visao
from noticias import Noticia

menu = """
        As seguintes opções estão disponíveis: 
            
        Imitar, capacidade de reproduzir sons emitidos pelos humanos
        
        VISÃO, iniciar módulo de visão computacional
        
        Contagem, realizar cálculos matemáticos
        
        Notícia, Recupera notícias da internet
        
        Finalizar, interromper interação com humanos
                        
        Para voltar ao Menu, diga, Menu        

"""


class Menu():
    
    def __init__(self):
        self.objOuvir = Audicao()
        self.objFala = Fala()
        # self.objMat = Matematica()
        # self.objVisao = Visao()    
        self.objNoticia = Noticia()
        self.flagContinuar = True

    def informaMenu(self):
        self.objFala.falar(menu)

    def imitar(self): #Reproduz o que a pessoa falar
        self.objFala.imitar()
    
    def ver(self): #inicia Câmera, incluir submenus
        self.objVisao.start()
    
    def contagem(self): #realiza algum calculo
        self.objMat.start()
        
    def noticias(self): #Realiza consulta no feed de noticias
        self.objNoticia.start()
    
    def sair(self):
        self.objFala.falar("Terminando operações, até mais senhor")
        self.flagContinuar = False
    
    def start(self):
        while not self.objOuvir.evocacao():
            pass
        self.objFala.falar('Estou aqui, senhor!')
        self.menu()
        
    def comandos(self,comando):
        try: 
            if comando == 'IMITAR':
                self.imitar()
            elif comando == 'VISÃO':
                self.ver()
            elif comando == 'CONTAGEM':
                self.contagem()
            elif comando  == 'MENU':
                self.informaMenu()
            elif comando == 'NOTÍCIA':
                self.noticias()
            elif comando  == 'FINALIZAR':
                self.sair()
            else:
                pass
        except Exception as err:
            try:
                self.objFala.falar(err)
            except Exception as err_fala:
                print(err_fala)
        
    def menu(self):
        while self.flagContinuar:
            self.comandos(self.objOuvir.ouvir())
            