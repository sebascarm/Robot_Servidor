# -*- coding: utf-8 -*-

###########################################################
### Clase GESTOR DE COMUNICACION ENTRE COMP  V1.1       ###
###########################################################
### ULTIMA MODIFICACION DOCUMENTADA                     ###
### 20/10/2020                                          ###
### Creacion de clase                                   ###
###########################################################

from componentes.thread_admin import ThreadAdmin
import time
from queue import Queue

from componentes.comunicacion import Comunicacion
from compuesto.image_send import Image_Send
from compuesto.robot_cara import Robot_Cara
from compuesto.robot_cuerp import Robot_Cuerpo
# Sensores
from sensores.ultrasonido import UltraSonido

from ia.tts import TTS

COLA_SONICO = Queue()
TH_SONICO   = ThreadAdmin()

class Gestor(object):
    def __init__(self):
        self.tcp_gestor = Comunicacion()
        self.host       = "127.0.0.1"
        self.log        = self.__log_default   # Para configurar log
        # Elementos de gestion
        self.im_send    = Image_Send()
        self.cara       = Robot_Cara()
        self.cuerpo     = Robot_Cuerpo()
        self.voz        = ''                   # type: TTS
        self.sonico_cent = UltraSonido()

    def config(self, host, voz):
        # type: (str, TTS)->None
        self.host = host
        # conexion del Gestor
        self.tcp_gestor.config(host, cliente=False, callback=self.__call_conexion)
        # Modulos de gestion
        self.im_send.config(host=host, port=50002)  # Imagen send
        self.cara.config()                          # Cara
        self.cara.config_cuerpo(self.cuerpo)        # datos del cuerpo a la cara
        self.cuerpo.config()                        # Cuerpo
        self.voz = voz
        # SENSORES
        self.sonico_cent.config(26, 19)  # pines trigger y echo

    def config_log(self, Log):
        """posibilidad de configurar clase Log(Texto, Modulo)"""
        self.log = Log.log
        # Imagen send
        self.im_send.config_log(Log)

    def iniciar(self):
        self.log("INICIANDO GESTOR", "GESTOR")
        # Gestor
        self.tcp_gestor.iniciar()

    ############################
    ### RECEPCION DE DATOS   ###
    ############################
    def __call_conexion(self, codigo, mensaje):
        if codigo == 2: # Conectado
            self.log("CONECTADO A GESTOR", "GESTOR")
            self.voz.say("Conexion establecida")
            # Imagen send
            self.im_send.iniciar()
        elif codigo == 4:   # Recepcion de datos
            self.recepcion_datos(mensaje)
        elif codigo != 3:   # 3 es envio de datos
            self.log("COD: " + str(codigo) + " Men: " + str(mensaje), "GESTOR")

    # Log por defecto
    def __log_default(self, Texto, Modulo):
        print(Texto)

    ###########################################################
    ### PROCESAMIENTO DE DATOS RECIBIDOS                    ###
    ###########################################################
    def recepcion_datos(self, datos):
        print(datos)
        splitted = datos.split("|")
        if len(splitted) == 1:          # acciones de un solo valor
            self.accion_unica(datos)
        else:
            modulo, comando, valor = datos.split("|")
            self.acciones(modulo, comando, valor)

    ########################################
    ### ANALISIS DE DATOS DE 1 VALOR     ###
    ########################################
    def accion_unica(self, comando):
        if comando == "[SONICO-ON]":
            TH_SONICO.start(self.hilo_sonico, COLA_SONICO, 'ENVIO_SONICO')
        if comando == "[SONICO-OFF]":
            TH_SONICO.close()

    ########################################
    ### ANALISIS DE RECEPCION DE DATOS   ###
    ########################################
    def acciones(self, modulo, comando, valor):
        # Selecccion segun modulo
        if modulo == "FACE":
            self.modulo_FACE(comando, valor)


    def modulo_FACE(self, comando, valor):
        # Seleccion segun comando
        if comando == "CENTRAR":
            val_x, val_y = valor.split("/")     # seperador de valores /
            val_x = int(int(val_x) * -0.2)
            val_y = int(int(val_y) * -0.2)
            # Mover la cara
            self.cara.mover(int(val_x), int(val_y))


    ########################################
    ### HILOS                            ###
    ########################################
    def hilo_sonico(self, cola_tiempo):
        tiempo = 1

        while self.tcp_gestor.conexion:
            # distancia = config.SONICO.distancia()
            distancia = self.sonico_cent.distancia_precisa(20)
            if distancia > -1:
                self.tcp_gestor.enviar("[SONICO:" + str(distancia) + "]")
            time.sleep(tiempo)
            # revisar cola
            if cola_tiempo.qsize() > 0:
                tiempo = float(cola_tiempo.get())
        print("EXIT SEND DISTANCIA")
