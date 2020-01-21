# -*- coding: utf-8 -*-

############################################################
### FUNCIONES VARIAS V 1.1                               ###
############################################################
### ULTIMA MODIFICACION DOCUMENTADA                      ###
### 21/01/2020                                           ###
### Funcion Windows o Linux                              ###
### Funcion Path_Actual                                  ###
############################################################
import os

def GetChkSum(strData):
	# Devuelve el Checksum de una cadena dada
    chksum = 0
    chksum = chksum	^ (int(str(int("20", 16)), 10))
    chksum = chksum	^ (int(str(int("03", 16)), 10))
    for char in strData:
	    chksum = chksum ^ ord(char)
    chksum = chksum	^ (int(str(int("04", 16)), 10))
    return chksum

def Val_to_text(valor, caracteres):
    # Devuelve en texto un valor completando con ceros
    # valor: numero ingresado
    # caracteres: la cantidad fija de caracteres a utilizar
    resul = ''
    dife = caracteres - len(str(valor))
    if dife > 0:
        for i in range(0, dife):
            resul += "0" 
        resul += str(valor)
    elif dife < 0:
        resul = str(valor)[-caracteres]
    else:
        resul = str(valor)
    return resul

def Path_Actual(Parametro__file__):
    # enviar solo variable __file__ sin ningun elemento
    return os.path.dirname(Parametro__file__)

def Windows():
    # retorna si el sistema operativo es windows
    if os.name == 'nt':
        return True
    else:
        return False