# -*- coding: utf-8 -*-

###########################################################
### CLASE TIMER V1.1                                    ###
###########################################################
### ULTIMA MODIFICACION DOCUMENTADA                     ###
### 05/02/2020                                          ###
### Mejora en FPS y Delay                               ###
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
        # Solo se puede usar un metodo x vez (o transcurrido o fps)
        # Cuenta el tiempo transcurrido y 
        # vuelve a 0 el contador
        #self.fin = datetime.now()
        self.fin = time.time()
        self.transc = self.fin - self.ini
        self.ini = self.fin
        return self.transc

    def fps(self):
        # Solo se puede usar un metodo x vez (o transcurrido o fps)
        transc = self.transcurrido()
        if (transc > 0.0):
            return 1 / (transc)
            #return (1 / (self.transcurrido()))
        else:
            return 0

    def delay(self, fps_requerido):
        #realiza pausa necesaria para completar los fps requeridos
        tiempo_requerido = 1 / fps_requerido
        self.delay_fin = time.time()
        self.delay_transc = self.delay_fin - self.delay_ini
        tiempo_pendiente = tiempo_requerido - self.delay_transc
        if tiempo_pendiente > 0:
            time.sleep(tiempo_pendiente)
        self.delay_ini = self.delay_fin + tiempo_pendiente
 

    