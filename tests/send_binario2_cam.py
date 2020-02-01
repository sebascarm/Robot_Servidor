""" Prueba de uso de binarios """
import time
# Esto es para poder hacer el from desde un nivel atras y funciona con launch.json
import os, sys
BASE_PATH = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(BASE_PATH)

from componentes.servidor_tcp import Servidor_TCP
from componentes.webcam import Webcam
from componentes.thread_admin import ThreadAdmin

th_cam = ThreadAdmin()
tcp = Servidor_TCP()
cam = Webcam()
cam.config(0,ModoActivo=True)
cam.start()

time.sleep(1)

def fun_calback(Codigo, Mensaje):
    if Codigo != 3:
        print("COD: ", Codigo, "Men: ", Mensaje)
    if Codigo == 2:
        th_cam.start(th_camara,'','CAMARA ENVIO')
            

def th_camara():
    time.sleep(2)
    while True:
        frame = cam.read()
        tcp.enviar(frame)
        time.sleep(0.1)


tcp.config(Host="192.168.0.26", Callback=fun_calback,Binario=True)
tcp.iniciar()

time.sleep(1000)
