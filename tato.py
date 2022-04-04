#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import serial
import time

class Tato():
    
    
    def __init__(self):
        
        self.objSerial = serial.Serial()
            
        self.objSerial.port = '/dev/ttyACM1'
        self.objSerial.baudrate = 9600
        self.objSerial.rtscts = True
        self.objSerial.dsrdtr = True
        self.objSerial.timeout = 5
    def iniciarMovimento(self):
        
        try:
            if self.objSerial.isOpen():
                self.objSerial.write(b'1')
            else:
                self.objSerial.open()
                time.sleep(1)
                self.objSerial.write(b'1')
            self.objSerial.flush()
        except Exception:
            
            raise Exception('Não foi possível comunicação serial.')
            
    def finalizarMovimento(self):
        try:
            self.objSerial.write(b'0')
            self.objSerial.flush()
            self.objSerial.close()
        except Exception:
            
            raise Exception('Erro ao interromper comunicação.')
        

