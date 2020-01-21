# -*- coding: utf-8 -*-

###########################################################
### CLASE TIMER V1.0                                    ###
###########################################################
### ULTIMA MODIFICACION DOCUMENTADA                     ###
### 08/01/2020                                          ###
###########################################################

#from datetime import datetime
import time

class Timer(object):
    def __init__(self):
        self.ini          = 0.0
        self.fin          = 0.0
        self.transc       = 0.0

        self.delay_ini    = 0.0
        self.delay_fin    = 0.0
        self.delay_transc = 0.0



    def iniciar(self):
        #self.ini = datetime.now()
        self.ini       = time.time()
        self.delay_ini = time.time()

    def transcurrido(self):
        # Cuenta el tiempo transcurrido y 
        # vuelve a 0 el contador
        #self.fin = datetime.now()
        self.fin = time.time()
        self.transc = self.fin - self.ini
        return self.transc

    def fps(self):
        return int(1 / (self.transcurrido()))
        #return (1 / (self.transcurrido()))

    def delay(self, fps_requerido):
        #pausa necesaria para completar los fps requeridos
        tiempo_requerido = 1 / fps_requerido
        self.delay_fin = time.time()
        self.delay_transc = self.delay_fin - self.delay_ini
        
        tiempo_pendiente = tiempo_requerido - self.delay_transc
        pend_ms          = tiempo_pendiente * 1000
        #print("pendiente", pend_ms)
        if pend_ms > 0:
            return int(pend_ms)
        else:
            return 0

    