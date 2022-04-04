#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from math import sqrt
from fala import Fala
from audicao import Audicao

menu_operacao = """
                As seguintes operações estão disponíveis,
                Soma,
                Subtração,
                Divisão,
                Multiplicação,
                Potência,
                e,
                Raiz Quadrada,

                Para repetir, diga, MENU,
            
                Para voltar ao menu principal, diga, voltar                

"""

class Matematica():
        
    dic_operacoes = {
        
        'SOMA' : lambda x,y : float(x)+float(y),
        'SUBTRAÇÃO' : lambda x,y : float(x)-float(y),
        'MULTIPLICAÇÃO' : lambda x,y : float(x)*float(y),
        'DIVISÃO' : lambda x,y : float(x)/float(y), #Observar divisao por zero
        'POTÊNCIA' : lambda x,y : float(x)**float(y),
        'RAIZ QUADRADA' : lambda x,y : sqrt(float(x)) #faz nada com y
        
    }
    
    def __init__(self):
        self.objFala = Fala()
        self.objOuvir = Audicao()
     
    
    def start(self):
        try:
            self.objFala.falar(menu_operacao)
            
            while True:            
            
            
                self.objFala.falar("Informe a operação:")
                self.operacao = self.objOuvir.ouvir()
                
                if self.operacao == 'MENU':
                    self.objFala.falar(menu_operacao)
                    continue
                elif self.operacao == 'VOLTAR':
                    break
                
                
                
                self.segundo_operador = ""
                self.objFala.falar("Informe o primeiro operador:")
                self.primeiro_operador = self.objOuvir.ouvir()
                
                if not self.isRaizQuadrada(self.operacao):
                    self.objFala.falar("Informe o segundo operador:")
                    self.segundo_operador = self.objOuvir.ouvir()
                
            
            
                self.retorno = self.realizaOperacao(self.operacao,self.primeiro_operador,self.segundo_operador)
                self.falaResultado(self.operacao,self.primeiro_operador,self.segundo_operador,self.retorno)
            
        except Exception as err:
            raise err
        
        
        
    
      
    def falaResultado(self,operacao,operador1,operador2,resultado):
        
        if not self.isRaizQuadrada(operacao):
            saida_resultado = "O resultado da operação, {}, com os operadores, {}, e, {}, é:, {}".format(operacao,operador1,operador2,"%.2f"%resultado)
        else:
            saida_resultado = "O resultado da operação, {}, com o operador, {}, é:, {}".format(operacao,operador1,"%.2f"%resultado)

        self.objFala.falar(saida_resultado)
    
    def realizaOperacao(self,operacao,x,y):
        
        try:
            
            self.validaOperacao(operacao)
            self.validaOperadores(x ,y)
            
            if 'DIVISÃO' == operacao:
                self.validaDivisao(y)
            
            
            resultado = self.dic_operacoes[operacao](x,y)
                       
            
            return resultado
        
        except Exception as err:
            raise err

    
        
    def validaDivisao(self,y):
        if y == '0':
            raise Exception('Divisão por zero, não permitida.')

    def validaOperacao(self,operacao):
        if (operacao is None) or (operacao not in self.dic_operacoes.keys()):
            raise Exception('Operação não permitida.')
        
        y = ""
        
        
    def validaOperadores(self,x,y):
        try:
            float(x)
            float(y)
        except Exception:
            raise Exception('Identificada alguma sentença não numérica em algum operador.')
        

    def isRaizQuadrada(self,operacao):
        return ( True if operacao == "RAIZ QUADRADA" else False )
            