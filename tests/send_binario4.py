""" Prueba de uso de binarios """
import time
# Esto es para poder hacer el from desde un nivel atras y funciona con launch.json
import os, sys
BASE_PATH = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(BASE_PATH)

from componentes.servidor_tcp import Servidor_TCP
from componentes.webcam import Webcam
from componentes.thread_admin import ThreadAdmin
from componentes.timer import Timer

th_cam  = ThreadAdmin()
tcp     = Servidor_TCP()
cam     = Webcam()
tiempo = Timer()

cam.config(0,ModoActivo=False)
cam.start()

time.sleep(1)

def fun_callback(Codigo, Mensaje):
    if Codigo != 3:
        print("COD: ", Codigo, "Men: ", Mensaje)
    if Codigo == 2:
        pass
        #th_cam.start(th_camara,'','CAMARA ENVIO',enviar_ejecucion=True)
            

def th_camara(run):
    time.sleep(2)
    tiempo.iniciar()
    while run.value:
        frame = cam.read()
        tcp.enviar(frame)
        print(tiempo.fps())
        tiempo.delay(10)


tcp.config(Host="192.168.0.34", Callback=fun_callback,Binario=True)     # PC LOCAL
#tcp.config(Host="127.0.0.1", Puerto=50001, Callback=fun_callback, Binario=True)
tcp.iniciar()

time.sleep(5)
print("fin")
quit()

