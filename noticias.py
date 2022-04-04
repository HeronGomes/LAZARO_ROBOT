# -*- coding: utf-8 -*-

import feedparser
import re
import nltk
from nltk.corpus import stopwords
import string
import spacy
import pandas as pd
from datetime import datetime

from fala import Fala
from audicao import Audicao

menu_operacao = """
                Informe, de forma breve, o assunto a ser pesquisado ,
                
                ou
                
                Para repetir, diga, MENU,
            
                Para voltar ao menu principal, diga, voltar                

"""
nltk.download('rslp')
nltk.download('stopwords')
class Noticia():
    
    noticias_leitura = []
    lista_feeds = []
    lista_valores = []
    stemmer_noticia = []
    feeds = []
    nlp = None
    stemmer = None
    queryTexto = None
    audicao = None
    fala = None
    resultado = None
    
    def __init__(self):
        
        self.objAudicao = Audicao()
        self.objFala = Fala()
        
        feeds_url = ['http://g1.globo.com/dynamo/brasil/rss2.xml', #Nivel Brasil
             'http://g1.globo.com/dynamo/loterias/rss2.xml',#Loterias
             'http://g1.globo.com/dynamo/mundo/rss2.xml', #Mundial
             'http://g1.globo.com/dynamo/tecnologia/rss2.xml',#Tecnologia e games
             'http://g1.globo.com/dynamo/minas-gerais/triangulo-mineiro/rss2.xml',  #Triangulo Mineiro
             'http://g1.globo.com/dynamo/ciencia-e-saude/rss2.xml', #Ciência e saude
             'http://g1.globo.com/dynamo/educacao/rss2.xml'] #Edução
        for url in feeds_url:
            self.feeds.append(feedparser.parse(url))
        
        self.nlp = spacy.load('pt_core_news_lg')
        
        self.stemmer = nltk.stem.RSLPStemmer()
        
    
    def pre_processamento(self,consulta):
    
        #Remove tag invalida
        corpus_alt = None
        texto_splitado = re.split("<br />", consulta)
        
        if(len(texto_splitado)>1):
            consulta = texto_splitado[1]
        
        #token
        corpus_alt = re.findall(r"\w+(?:'\w+)?|[^\w\s]",consulta)
        
        #aplicar lower
        corpus_alt = [t.lower() for t in corpus_alt]
    
        #remove stops
    
        palavras_stops = stopwords.words('portuguese')
    
        corpus_alt = [p for p in corpus_alt if p not in palavras_stops]
    
        #remove numero
        corpus_alt = [re.sub(r'\d','',p) for p in corpus_alt]
    
        #remove pontuacoes
        corpus_alt = [p for p in corpus_alt if p not in string.punctuation]
        
        return corpus_alt
    
    def ajuste_leitura(self,consulta):
    
        texto_splitado = re.split("<br />", consulta)
        
        if(len(texto_splitado)>1):
            consulta = texto_splitado[1]
            
        return consulta.lower()
    
    def jaccard_similarity(self,list1,list2):
      s1 = set(list1)
      s2 = set(list2)
      # print('Intersecação:',len(s1.intersection(s2)))
      # print('União:',len(s1.union(s2)))
            
      return len(s1.intersection(s2)) / len(s1.union(s2))
  
    #pega apenas os feeds do dia
    def isDataAtual(self,feedParam):
        _,dia,mes,ano,_,_ = feedParam['published'].split()
        nova_data = datetime.strptime(dia+'/'+mes+'/'+ano, '%d/%b/%Y').strftime('%d/%b/%Y') 
        return nova_data == datetime.today().strftime('%d/%b/%Y')
    
    
    def trata_noticias(self):
    
        self.lista_feeds = [texto for feed in self.feeds for texto in feed['entries']] 
        self.noticias_leitura = [self.ajuste_leitura(feed['summary']) for feed in self.lista_feeds]
        noticias_tratadas = [self.pre_processamento(feed['summary']) for feed in self.lista_feeds]
        for noticia in noticias_tratadas:
    
            stemmers = [ self.stemmer.stem(token) for token in noticia]
            self.stemmer_noticia.append(stemmers)
    
    
    def trata_consulta(self,consulta):
        self.queryTexto = self.pre_processamento(consulta)
        self.queryTexto = [self.stemmer.stem(token) for token in self.queryTexto]
        
        print('##########################################\n')
        print('Palavras chave para consulta\n')
        print(self.queryTexto)
        print('\n')
        print('##########################################\n')
    
    
    def calcula_similaridade(self):
        for i,leitura in  enumerate(self.stemmer_noticia):    
            valor = self.jaccard_similarity(leitura,self.queryTexto)
            # print('Notícia número ',i,' com similaridade: ',valor)
            if valor > 0 and valor is not None:
                self.lista_valores.append([valor,self.lista_feeds[i]['title'],self.noticias_leitura[i]])

        if not self.lista_valores:
            self.lista_valores.append([0,'Pesquisa não retornou nenhum dado','Pesquisa não retornou nenhum dado'])


        resultado = pd.DataFrame(self.lista_valores,columns=('Similaridade','titulo','noticia'))


        return resultado.nlargest(3,'Similaridade','first')
        
    def processa_noticia(self,consulta):
        
        self.trata_consulta(consulta)
        self.trata_noticias()
        
        self.resultado = self.calcula_similaridade()
        
        print('##########################################\n')
        print('Tabela de similaridade\n')
        print(self.resultado)
        print('\n')
        print('##########################################\n')
        
        for noticia in self.resultado['noticia']:
            self.objFala.falar(noticia)
    
    def start(self):
        
        try:
            
            self.objFala.falar('O que o senhor, gostaria de pesquisar?')
                    
            while True:
                
                self.comando = self.objAudicao.ouvir()
                                    
                if self.comando == 'MENU':
                    self.objFala.falar(menu_operacao)
                    continue
                elif self.comando == 'VOLTAR':
                    break
                elif self.comando:
                    self.processa_noticia(self.comando)
                    self.objFala.falar('Fim das notícias, o que devo fazer?')
                
        except Exception as err:
            raise err
    
    
    
    
    
    