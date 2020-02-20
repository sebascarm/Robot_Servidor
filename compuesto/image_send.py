# -*- coding: utf-8 -*-

###########################################################
### IMAGEN COMPUESTO V1.0                               ###
###########################################################
### ULTIMA MODIFICACION DOCUMENTADA                     ###
### 19/02/2020                                          ###
### Creacion                                            ###
###########################################################

import time
from componentes.comunicacion import Comunicacion
from componentes.webcam import Webcam
from componentes.thread_admin import ThreadAdmin
from componentes.timer import Timer


class Image_Send(object):
    def __init__(self):
        self.camara     = Webcam()
        self.tcp        = Comunicacion()
        self.host       = "127.0.0.1"
        self.reintentos = 10            # cantidad de reintentos de conexion de la camara
        self.th_cam     = ThreadAdmin() # Thread para la camara
        self.tiempo     = Timer()       # Control de fps
        self.log = self.__log_default   # Para configurar log

    def config(self, host):
        self.host = host
        self.camara.config()            # usamos los valores por defecto (El modo activo tiene menos delay)
        self.tcp.config(host, cliente=False, binario=True, callback=self.__call_conexion)

    def config_log(self, Log):
        '''posibilidad de configurar clase Log(Texto, Modulo)'''
        self.log = Log.log
        self.camara.config_log(Log)          # enviamos el log configurado a la camara tambien

    def iniciar(self):
        self.camara.start()
        if self.camara.activo:  # CONEXION EXITOSA
            self.log("CAMARA CONECTADA","IMAGE-SEND")
            self.tcp.iniciar()
        else:
            self.log("CAMARA SIN CONEXION", "IMAGE-SEND")

    def __call_conexion(self, codigo, mensaje):
        if codigo != 3:  # 3 es envio de datos
            self.log("COD: " + str(codigo) + " Men: " + str(mensaje), "IMAGE-SEND")
        if codigo == 2:
            self.th_cam.start(self.__th_camara, '', 'CAMARA ENVIO',callback=self.__log_th, enviar_ejecucion=True)

    def __th_camara(self, run):
        self.tiempo.iniciar()
        while self.tcp.conexion and run.value:
            frame = self.camara.read()  # Lectura de cuadro de camara
            self.tcp.enviar(frame)      # Enviar cuadro
            # print(self.tiempo.fps())    # ver los fps que enviamos (solo envia 5 cuadros la raspberry)
            self.tiempo.delay(6)

    # Log por defecto
    def __log_default(self, Texto, Modulo):
        print(Texto)

    # Log que devuelve el thread
    def __log_th(self, Codigo, Mensaje):
        self.log(Mensaje, "IMAGE-SEND")