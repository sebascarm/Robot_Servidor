# -*- coding: utf-8 -*-

###########################################################
### RECEPCION_TCP V1.0                                  ###
###########################################################
### ULTIMA MODIFICACION DOCUMENTADA                     ###
### 29/09/2019                                          ###
###                                                     ###
###########################################################

from thread_admin import ThreadAdmin
import time
from queue import Queue

import config   #variables globales

COLA        = Queue()
TH_COMPAS   = ThreadAdmin()
COLA_SONICO = Queue()
TH_SONICO   = ThreadAdmin()

def recepcion_tpc(mensaje):
    # print(mensaje)
    # partimos para obtener parametros en caso de recibirlos
    mensaje_split = str(mensaje).split(":",1) 
    if mensaje == "[COMPAS-ON]":
        TH_COMPAS.start(hilo_compas, COLA,'ENVIO_ANGULO')
    if mensaje == "[COMPAS-OFF]":
        TH_COMPAS.close()
    
    if mensaje == "[SONICO-ON]":
        TH_SONICO.start(hilo_sonico, COLA_SONICO,'ENVIO_SONICO')
    if mensaje == "[SONICO-OFF]":
        TH_SONICO.close()
        
    #recepcion de 2 valores (parametros)
    if len(mensaje_split) > 1:  
        if mensaje_split[0] == "[COMPAS-SPEED]":
            print (mensaje_split[1])
            COLA.put(mensaje_split[1])
        
        if mensaje_split[0] == "[SONICO-SPEED]":
            print (mensaje_split[1])
            COLA_SONICO.put(mensaje_split[1])
        


def hilo_compas(cola_tiempo):
    tiempo = 1
    while config.TCP.conexion:
        angulo = config.COMPAS.angulo()
        #print("SEND: " + str(angulo))
        config.TCP.enviar("[COMPAS:" + str(angulo) + "]")
        time.sleep(tiempo)
        #revisar cola
        if cola_tiempo.qsize() > 0:
            tiempo = float(cola_tiempo.get())
    print ("EXIT SEND COMPAS")

def hilo_sonico(cola_tiempo):
    tiempo = 1
    while config.TCP.conexion:
        #distancia = config.SONICO.distancia()
        distancia = config.SONICO.distancia_precisa(20)
        if distancia > -1:
            config.TCP.enviar("[SONICO:" + str(distancia) + "]")
        time.sleep(tiempo)
        #revisar cola
        if cola_tiempo.qsize() > 0:
            tiempo = float(cola_tiempo.get())
    print ("EXIT SEND DISTANCIA")
    
