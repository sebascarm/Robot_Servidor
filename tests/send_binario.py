""" Prueba de uso de binarios """
import time
# Esto es para poder hacer el from desde un nivel atras y funciona con launch.json
import os, sys
BASE_PATH = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(BASE_PATH)

from componentes.servidor_tcp import Servidor_TCP

import cv2

tcp = Servidor_TCP()

# si es windows
captura             = cv2.VideoCapture(0, cv2.CAP_DSHOW)
time.sleep(2)
procesado, frame    = captura.read()
captura.release()

def fun_calback(Codigo, Mensaje):
    print("COD: ", Codigo, "Men: ", Mensaje)
    if Codigo == 2:
        #conectado
        print("conectado enviar")
        print ("SYS: ", sys.getsizeof(frame))
        print("FRAME: ", (frame))
        tcp.enviar(frame)


tcp.config(Callback=fun_calback,Binario=True)
tcp.iniciar()

time.sleep(1000)
