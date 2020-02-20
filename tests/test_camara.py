# Esto es para poder hacer el from desde un nivel atras
import sys
sys.path.append("..")

from ia.camara import Camara


camara = Camara()
camara.config(Resolucion=(640,480),Frames=30, Visible=True)
camara.iniciar()

