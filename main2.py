# -*- coding: utf-8 -*-

###########################################################
### MAIN2 V1.1                                          ###
###########################################################
### ULTIMA MODIFICACION DOCUMENTADA                     ###
### 26/02/2020                                          ###
###########################################################

import time
from ia.tts import TTS

from componentes.logg import Logg
from compuesto.gestor import Gestor
#from compuesto.image_send import Image_Send
# from actividad.actividad import Actividad

log = Logg()
log.definir()

voz = TTS()
voz.config(Log=log)

#im_send = Image_Send()
gestor = Gestor()

def inicio():
    log.log("Main start", "MAIN")
    voz.say("Iniciando Robot")
    gestor.config("192.168.0.24", voz)
    voz.say("Esperando conexion en I P 192.168.0.24")
    gestor.config_log(log)
    gestor.iniciar()

if __name__ == "__main__":
    inicio()
    time.sleep(10000)
    log.log("Exit Robot", "MAIN")