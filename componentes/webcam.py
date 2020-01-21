# -*- coding: utf-8 -*-

###########################################################
### Clase WEBCAM V1.0                                   ###
###########################################################
### ULTIMA MODIFICACION DOCUMENTADA                     ###
### 21/01/2020                                          ###
### Creacion de clase                                   ###
###########################################################

import cv2
import time
from componentes.thread_admin import ThreadAdmin

class Webcam(object):
    def __init__(self):
        #inicializar y leer el primer cuadro
        self.captura     = ''
        self.procesado   = False
        self.frame       = ''
        self.activo      = False
        self.th_capturar = ThreadAdmin()
        self.log         = self.__log_default
        self.src         = 0 
        self.sleeptime   = 0.01

    def config(self, src=0):
        self.src = src

    def config_log(self, Log):
        #posibilidad de configurar clase Log(Texto, Modulo)
        self.log = Log.log

    def start(self):
        self.log("Inicializando Webcam", "WEBCAM")
        self.captura = cv2.VideoCapture(self.src, cv2.CAP_DSHOW)
        self.log("Webcam Inicializada", "WEBCAM")
        (self.procesado, self.frame) = self.captura.read()
        self.activo = True
        self.th_capturar.start(self.__th_loop,'','WEBCAM', callback=self.__callaback_th)

    def stop(self):
        self.activo = False
        self.log("Webcam Stop", "WEBCAM")
   
    def read(self):
        return self.frame

    def check(self):
        self.captura = cv2.VideoCapture(self.src, cv2.CAP_DSHOW)
        if self.captura.isOpened():
            self.captura.release()
            self.log("Webcam disponible", "WEBCAM")
            return True
        else:
            self.captura.release()
            self.log("Webcam no disponible", "WEBCAM")
            return False

    def __th_loop(self):
        while self.activo:
            if self.captura.isOpened():
                # leer cuadro
                (self.procesado, tmp_frame) = self.captura.read()
                if self.procesado:
                    self.frame = tmp_frame
                else:
                    self.log("Frame Error", "WEBCAM")
            else:
                self.log("Camara Error", "WEBCAM")
            # descansar
            time.sleep(self.sleeptime)
        # cierre
        self.captura.release()
        self.log("Webcam Stoped", "WEBCAM")

    # Log por defecto
    def __log_default(self, Texto, Modulo):
        print(Texto)
    
    # Callback de TH
    def __callaback_th(self, Codigo, Mensaje):
        self.log(Mensaje, "WEBCAM")
            
