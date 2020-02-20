# -*- coding: utf-8 -*-

###########################################################
### MAIN2 V1.1                                          ###
###########################################################
### ULTIMA MODIFICACION DOCUMENTADA                     ###
### 19/02/2020                                          ###
###########################################################

import time

from componentes.logg import Logg
from compuesto.image_send import Image_Send
# from actividad.actividad import Actividad

log = Logg()
log.definir()

im_send = Image_Send()

def inicio():
    log.log("Main start", "MAIN")
    # INCIAR MODULO COMPUESTO
    im_send.config("192.168.0.24")
    im_send.config_log(log)
    im_send.iniciar()

if __name__ == "__main__":
    inicio()
    time.sleep(1000)
    log.log("Exit Robot", "MAIN")