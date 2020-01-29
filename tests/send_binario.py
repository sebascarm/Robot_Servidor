""" Prueba de uso de binarios """
import time
# Esto es para poder hacer el from desde un nivel atras y funciona con launch.json
import os, sys
BASE_PATH = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(BASE_PATH)

from componentes.servidor_tcp import Servidor_TCP

import cv2

tcp = Servidor_TCP()


#captura = cv2.VideoCapture(0, cv2.CAP_DSHOW) # si es windows
captura  = cv2.VideoCapture(0) # si es linux

time.sleep(1)
#while True:
#    if captura.isOpened():
#        print("opne")
#        procesado, frame    = captura.read()
#        if procesado:
#            print("procesadi")
#            cv2.imshow('frame',frame)
#            cv2.waitKey(1) 
        ## Salir con Q
        #key = cv2.waitKey(1) & 0xFF
        #if key == ord("q"):
        #    break 
    # descansar
        #time.sleep(0.1)


procesado, frame    = captura.read()
captura.release()


def fun_calback(Codigo, Mensaje):
    print("COD: ", Codigo, "Men: ", Mensaje)
    if Codigo == 2:
        #conectado
        #time.sleep(6)
        print("conectado enviar")
        #print ("SYS: ", sys.getsizeof(frame))
        #print("FRAME: ", (frame))
        tcp.enviar(frame)


tcp.config(Callback=fun_calback,Binario=True)
tcp.iniciar()

time.sleep(1000)
