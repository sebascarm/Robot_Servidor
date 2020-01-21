# -*- coding: utf-8 -*-

###########################################################
### CLASE LOGG V1.2                                     ###
###########################################################
### ULTIMA MODIFICACION DOCUMENTADA                     ###
### 20/01/2020                                          ###
### correcion Objeto de salida, opcion vacio            ###
### correcion en conversion str, puede variar con clie  ###
### Ajustes en la visualización de :                   ###
###########################################################

from datetime import datetime

class Logg(object):
    def __init__(self):
        self.linea = 0
        self.objeto_salida = ""

    def definir(self, Objeto_Salida=""):
        self.objeto_salida  = Objeto_Salida

    def log(self, texto, modulo =""):
        #tiempo = datetime.now().strftime('%H:%M:%S.%f')[:-3]
        tiempo = datetime.now().strftime('%H:%M:%S.%f')[:-3]
        salida = ""
        #Si es primera linea
        if modulo != "":
            modulo = " [" + modulo + "]"
        if self.linea == 0:
            salida =  str(tiempo) + " INICIO DE LOG " + modulo + "\n"
        
        salida += str(tiempo) + modulo + " " + str(texto) + "\n"
        self.linea += 1
        
        if self.objeto_salida == "":
            #si no se especifico un objeto de salida se envia a la pantalla
            print(salida, end = "")
        else:
            self.objeto_salida.text += salida
            


