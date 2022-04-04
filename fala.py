import pyttsx3
from audicao import Audicao
from tato import Tato

class Fala():
    
    def __init__(self):
        self.engine = pyttsx3.init('espeak')
        self.engine.setProperty('voice','brazil')
        self.engine.setProperty('rate',150)
        self.objAudicao = Audicao()
        self.objTato = Tato()
    
    def falar(self,frase):
        try:
            if frase is not None:
                self.objTato.iniciarMovimento()
                self.engine.say(frase)
                self.engine.runAndWait()
                self.objTato.finalizarMovimento()
        except Exception:
            raise Exception()

    def imitar(self):
        self.falar("Aguardando iteração humana.")
        frase = self.objAudicao.ouvir()
        self.falar(frase)