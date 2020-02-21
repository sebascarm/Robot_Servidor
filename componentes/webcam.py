# -*- coding: utf-8 -*-

###########################################################
### Clase WEBCAM V1.8                                   ###
###########################################################
### ULTIMA MODIFICACION DOCUMENTADA                     ###
### 21/02/2020                                          ###
### Desconexion de camara                               ###
### Revision de conexion                                ###
##  Estado de la camara                                 ###
### Camara sin conexion                                 ###
### Uso de nuevo Thread con salida                      ###
### Captura en modo activo y modo pasivo                ###
### Funcionamiento en windows y linux                   ###
### Creacion de clase                                   ###
###########################################################

import time
import imutils
import cv2
from componentes.thread_admin import ThreadAdmin
from componentes.funciones import Windows

class Webcam(object):
    def __init__(self):
        #inicializar y leer el primer cuadro
        self.captura     = ''       # cv2 video captura
        self.procesado   = False
        self.frame       = ''
        self.activo      = False    # Estado de la camara
        self.th_capturar = ThreadAdmin()
        self.log         = self.__log_default   # Para configurar log
        self.src         = 0 
        self.sleeptime   = 0.01
        self.modo_activo = True # Metodo activo donde la camara queda en loop constante // False solo captura en la peticion
        self.ancho       = 0    # devuelve valores por defecto
        self.alto        = 0    # devuelve valores por defecto
        self.reintento   = 10   # reintento de conexion

    def config(self, src=0, ModoActivo=True, Ancho=0, Alto=0, reint_conex=10):
        ''' reint_conex: Reintentos de conexion con la camara
            ModoActivo: Camara capturando en segundo plano (mas rapido en raspberry)
        '''
        self.src         = src
        self.modo_activo = ModoActivo
        self.ancho       = Ancho
        self.alto        = Alto
        self.reintento   = reint_conex

    def config_log(self, Log):
        '''posibilidad de configurar clase Log(Texto, Modulo)'''
        self.log = Log.log

    def start(self):
        # reintento de conexion a la camara
        for intento in range(0, self.reintento):
            self.log("Inicializando Webcam", "WEBCAM")
            if Windows():
                self.captura = cv2.VideoCapture(self.src, cv2.CAP_DSHOW)
            else:
                self.captura = cv2.VideoCapture(self.src)
            # Revisar si conecto la camara
            if self.captura.isOpened():
                self.log("Webcam Inicializada", "WEBCAM")
                (self.procesado, self.frame) = self.captura.read()
                self.activo = True
                if self.modo_activo:
                    self.th_capturar.start(self.__th_loop,'','WEBCAM', callback=self.__callaback_th, enviar_ejecucion=True)
                # Salimos del reintento
                break
            else:
                self.log("Webcam (Falla en conexion)", "WEBCAM")
            time.sleep(2)  # pausa de 2 segundos para reintentar conexion

    def stop(self):
        if not self.modo_activo:
            self.captura.release()
        self.activo = False
        if self.modo_activo:
            self.th_capturar.close()
        self.log("Webcam Stop", "WEBCAM")
   
    def read(self):
        if self.modo_activo:
            return self.frame # devuelve imagen previamente capturada en el loop
        else:
            self.__captura()
            return self.frame # devuelve imagen capturada
    
    def check(self):
        ''' Controla si la webcam esta disponible
        '''
        if Windows():
            self.captura = cv2.VideoCapture(self.src, cv2.CAP_DSHOW)
        else:
            self.captura = cv2.VideoCapture(self.src)
        if self.captura.isOpened():
            self.captura.release()
            self.log("Webcam disponible", "WEBCAM")
            return True
        else:
            self.captura.release()
            self.log("Webcam no disponible", "WEBCAM")
            return False

    def __th_loop(self, run):
        while self.activo and run.value:
            self.__captura()
            time.sleep(self.sleeptime)  # descansar
        # cierre
        self.captura.release()
        self.log("Webcam Stoped", "WEBCAM")
    
    def __captura(self):
        if self.captura.isOpened():
            # leer cuadro
            (self.procesado, tmp_frame) = self.captura.read()
            if self.procesado:
                if self.ancho == 0:
                    self.frame = tmp_frame  # tamaño original
                else:
                    # tamaño ajustado
                    # print("ajustar tam")
                    self.frame = imutils.resize(tmp_frame, width=self.ancho, height=self.alto)
                    # print("ajustar tam ok")
            else:
                self.log("Frame Error", "WEBCAM")
                self.log("Posible camara desconectada", "WEBCAM")
                self.stop() # Frenar la camara para que no entre en loop
        else:
            self.log("Camara desconectada", "WEBCAM")
            self.activo = False # desactivamos la camara.

    # Log por defecto
    def __log_default(self, Texto, Modulo):
        print(Texto)
    
    # Callback de TH
    def __callaback_th(self, Codigo, Mensaje):
        self.log(Mensaje, "WEBCAM")
            
