# -*- coding: utf-8 -*-

###########################################################
### ACTIVIDAD V1.0                                      ###
###########################################################
### ULTIMA MODIFICACION DOCUMENTADA                     ###
### 04/01/2020                                          ###
###########################################################

from ia.tts import TTS
from comunicacion.comunic import Comunicacion

def Actividad(Log):
    tts = TTS()
    tts.config(24500, Log)
    tts.say("Iniciando Robot", "iniciando_robot.mp3")

    tts.say("Estableciendo comunicación remota en puerto 50001", "estableciendo_comunicacion.mp3")
    comun = Comunicacion()
    #comun.config("192.168.0.24", 50001)
    comun.config("192.168.0.34", 50001)
    comun.config_log(Log)
    comun.iniciar()
    tts.say("Comunicacion remota inicializada","comunicacion_establecida.mp3")