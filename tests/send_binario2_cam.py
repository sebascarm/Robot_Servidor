""" Prueba de uso de binarios """
import time
# Esto es para poder hacer el from desde un nivel atras y funciona con launch.json
import os, sys
BASE_PATH = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(BASE_PATH)

from componentes.servidor_tcp import Servidor_TCP
from componentes.webcam import Webcam

tcp = Servidor_TCP()
cam = Webcam()
cam.config(ModoActivo=False)
cam.start()

time.sleep(1)

def fun_calback(Codigo, Mensaje):
    print("COD: ", Codigo, "Men: ", Mensaje)
    if Codigo == 2:
        while True:
            frame = cam.read()
            tcp.enviar(frame)
            time.sleep(0.01)
    

tcp.config(Callback=fun_calback,Binario=True)
tcp.iniciar()

time.sleep(1000)
