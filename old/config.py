#Clases Generales
from comunicacion.comunic import Comunicacion

from Logs.logg import Logg  #log
#from conexion.servidor_tcp import Servidor_TCP
#sensores
from sensores.compas import Compas
from sensores.ultrasonido import UltraSonido

#Variables de alcance global
global COMUNIC  # clase global de comunicacion 
global LOGS
#global TCP
global COMPAS
global SONICO

LOGS    = Logg()
#TCP    = Servidor_TCP()
COMUNIC = Comunicacion()
COMPAS  = Compas()
SONICO  = UltraSonido()