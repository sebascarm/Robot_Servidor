# Esto es para poder hacer el from desde un nivel atras y funciona con launch.json

import os, sys
BASE_PATH = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(BASE_PATH)

import time

from ia.face_detect import Face_Detect
from componentes.logg import Logg

def callback():
    print("DETECTADO CALBACK")
def callback_cuadro(x, y, x2, y2):
    print("CUADRO", x, y, x2, y2)

def callback_vista(x,y):
    print("VISTA:", x,y)

def callback_centrar(x,y):
    print("CENT: ", x,y)

def callback_unica(x,y):
    print("UNICA: ", x,y)

log = Logg()

face = Face_Detect()
face.config(Resolucion=(320,240),Show=False)
face.config_log(log)
face.config_callback(Func_Unica=callback_unica)

cam = face.check()

if cam:
    face.iniciar()
    time.sleep(50)
    face.stop()
    time.sleep(5)
    