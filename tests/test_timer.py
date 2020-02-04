# Esto es para poder hacer el from desde un nivel atras y funciona con launch.json
import os, sys
BASE_PATH = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(BASE_PATH)

import time
from componentes.timer import Timer

tiempo = Timer()

tiempo.iniciar()

while True:
    print("FPS: ", tiempo.fps())
    tiempo.delay(1)
    