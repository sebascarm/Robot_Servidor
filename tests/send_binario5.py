""" Prueba de uso de binarios """
import time
# Esto es para poder hacer el from desde un nivel atras y funciona con launch.json
import os, sys

BASE_PATH = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(BASE_PATH)

from componentes.comunicacion import Comunicacion
from componentes.webcam import Webcam
from componentes.thread_admin import ThreadAdmin
from componentes.timer import Timer

th_cam = ThreadAdmin()
tcp = Comunicacion()
cam = Webcam()
tiempo = Timer()

cam.config(0, ModoActivo=True)
cam.start()
time.sleep(1)


def fun_callback(codigo, mensaje):
    if codigo != 3: # 3 es envio de datos
        print("COD: ", codigo, "Men: ", mensaje)
    if codigo == 2:
        th_cam.start(th_camara, '', 'CAMARA ENVIO', enviar_ejecucion=True)


def th_camara(run):
    time.sleep(2)
    tiempo.iniciar()
    while tcp.conexion and run.value:
        frame = cam.read()
        tcp.enviar(frame)
        print(tiempo.fps())
        tiempo.delay(10)


tcp.config("192.168.0.24", cliente=False, binario=True, callback=fun_callback)
tcp.iniciar()
time.sleep(1000)

# terminar siempre con esta sentencia
ThreadAdmin.close_all()
