#import ptvsd
#ptvsd.enable_attach(address=('192.168.0.26', 3000), redirect_output=True)
#Pause
#ptvsd.wait_for_attach()

import time
import config   #variables globales
from thread_admin import ThreadAdmin
from eventos_tcp.eventos import recepcion_tpc

from sensores.servo import Servo

config.LOGS.definir()

def inicio():
    config.LOGS.log("Iniciando robot")
    #config.TCP.configuracion(Callback_Conexion, "192.168.0.24", 50001)
    config.COMUNIC.config("192.168.0.24", 50001)
    config.COMUNIC.iniciar()
        
    config.SONICO.config(26, 19) # pines 
    
    config.COMUNIC.recepcion("<01|034|013|MODULO|COMANDO|123456>")
    config.COMUNIC.recepcion("<03|034|015|MODULO|COMANDO|123456>")
    #config.COMUNIC.recepcion("<03|039|082|MODO|COMO|1213123231223456>")
    #test servos
    #servo_test()
    
    
    while True:
        #loop infinito
        time.sleep(5)
   

if __name__ == "__main__":
    inicio()
    print("EXIT ROBOT")
