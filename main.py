# -*- coding: utf-8 -*-

###########################################################
### MAIN V1.0                                           ###
###########################################################
### ULTIMA MODIFICACION DOCUMENTADA                     ###
### 04/01/2020                                          ###
###########################################################

from componentes.logg import Logg
from actividad.actividad import Actividad

log = Logg()
log.definir()

def inicio():
    log.log("Main start", "MAIN")
    Actividad(log)

if __name__ == "__main__":
    inicio()
    log.log("Exit Robot", "MAIN")