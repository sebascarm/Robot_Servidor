# -*- coding: utf-8 -*-

###########################################################
### MAIN3 V1.3                                          ###
###########################################################
### ULTIMA MODIFICACION DOCUMENTADA                     ###
### Uso del gestor
### 17/10/2020                                          ###
###########################################################

import time
from ia.tts import TTS

from componentes.logg import Logg
from compuesto.gestor import Gestor
from componentes.comunic.servidor_tcp import obtener_ip

# from compuesto.image_send import Image_Send
# from actividad.actividad import Actividad

log = Logg()
log.definir()

voz = TTS()
voz.config(Log=log)

# im_send = Image_Send()
gestor = Gestor()
IP = obtener_ip()


def inicio():
    log.log("Main start", "MAIN")
    voz.say("Iniciando Robot")
    gestor.config(IP, voz)
    voz.say("Esperando conexion en I P " + IP)
    gestor.config_log(log)
    gestor.iniciar()


if __name__ == "__main__":
    inicio()
    time.sleep(10000)
    log.log("Exit Robot", "MAIN")