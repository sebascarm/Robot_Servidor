###########################################################
### CLASE ULTRASONIDO V1.2                              ###
###########################################################
### ULTIMA MODIFICACION DOCUMENTADA                     ###
### 20/10/2020                                          ###
### Utilizacion de modulo en PC                         ###
###########################################################

try:
    import RPi.GPIO as GPIO
    NO_ULTRA = False
except:
    print("Modulo Ultrasonico NO DISPONIBLE")
    NO_ULTRA = True
    import random

import time
import math

class UltraSonido (object):
    def __init__(self):
        self.GPIO_TRIGGER = 0
        self.GPIO_ECHO    = 0
 
    def config(self, gpio_Trigger, gpio_echo):
        #GPIO TRIGGER = PIN
        #GPIO ECHO    = PIN
        if not NO_ULTRA:
            GPIO.setmode(GPIO.BCM)
            print ("Inicializando ultrasonido")
            # Set pins as output and input
            self.GPIO_TRIGGER = gpio_Trigger
            self.GPIO_ECHO    = gpio_echo
            GPIO.setup(self.GPIO_TRIGGER, GPIO.OUT)  # Trigger
            GPIO.setup(self.GPIO_ECHO, GPIO.IN)      # Echo

    def distancia(self, espera_max=1, reintentar=True):
        if not NO_ULTRA:
            self.reintentar = reintentar
            salida = False
            #time.sleep(0.05)
            stop = time.time() + 1
            GPIO.output(self.GPIO_TRIGGER, False)
            time.sleep(0.000002)    # 2 microsegundos     (apagado) - calma de sensor
            GPIO.output(self.GPIO_TRIGGER, True)
            time.sleep(0.00001)     # 10 microsegundos    (encendido)
            GPIO.output(self.GPIO_TRIGGER, False)       # (apagado)
            #
            start1 = time.time()
            start = time.time()
            elapsed = 100000000000000

            while GPIO.input(self.GPIO_ECHO) == 0:
                start = time.time()
                elapsed1 = start - start1
                if elapsed1 > 0.1:  # salimos x error
                    print ("salio echo 0 (demoro mucho el inicio)")
                    salida = True
                    break

            while GPIO.input(self.GPIO_ECHO) == 1:
                stop = time.time()
                elapsed = stop - start
                if elapsed > espera_max:  # mayor a 17 metros se interrumpe (0.1)/ 17 metros es el limite / cambio a 8,5 metros 0.05
                    #print ("salio echo 1 (demoro mucho el sonido, mayor a  8,5 mts)")
                    #La proxima medicion va a tener error (3 - 4 cm)
                    salida = True
                    break

            if salida:
                distance = -1
            else:
                #elapsed = stop - start
                distance = elapsed * 34000
                distance = distance / 2
            #DISTANCIAS MAYORES A 250 CM PUEDEN TENER ERRORES
            #si la distancia es menor a 4 cm hay un error (sule suceder despues de medir una distancia muy larga)
            if (self.reintentar) and (distance < 4) and (distance > 0):
                #medimos nuevamente
                #print ("medir nuevamente por distancia = " + str(distance))
                distance = self.distancia(0.05, False)

            return distance

        else:
            # en caso de no tener sensor devuelve valor aleatorio entre 10 cm y 20 cm
            return random.randint(0, 400)

    def distancia_precisa(self, reintentos):
        distancia = [0,0]
        Loop = True
        intentos_int = 0
        intentos = 0
        while intentos < reintentos:
            while Loop:
                for i in range(2):
                    #time.sleep(0.15)
                    #time.sleep(0.05)
                    time.sleep(0.001) # 1 ms
                    distancia[i] = self.distancia()
                    #print "distancia " + str(i) + ": " + str(distancia[i])
                    diferencia = Valor_Absoluto(distancia[0] - distancia[1])
                    #print "diferencia: " + str(diferencia)
                    if (diferencia < 1):
                        #print "igualdad"
                        valor = (distancia[0] + distancia[1]) / 2
                        Loop = False
                    intentos_int = intentos_int + 1
                    if intentos_int == 20:
                        #valor = 0
                        valor = -1
                        Loop = False
            resultado = valor
            intentos = intentos + 1
            if resultado > 0:
                intentos = reintentos
            #time.sleep(0.1)
            time.sleep(0.001) # 1 ms
        return valor


# FUNCIONES INTERNAS

def Valor_Absoluto(x):
    if x < 0:
        return -x
    else:
        return x