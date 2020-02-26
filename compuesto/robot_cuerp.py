# -*- coding: utf-8 -*-

###########################################################
### ROBOT CUERPO V1.0                                   ###
###########################################################
### ULTIMA MODIFICACION DOCUMENTADA                     ###
### 26/02/2020                                          ###
### Creacion                                            ###
###########################################################
import time
from sensores.servo import Servo


class Robot_Cuerpo(object):
    def __init__(self):
        self.servo_izq = Servo()
        self.servo_der = Servo()

    def config(self):
        self.servo_izq.config_continuo(3, 351, 401, 301)
        self.servo_der.config_continuo(0, 353, 403, 303, invertir=True)

    def rotar_izq(self):
        """hace una rotacion por 0.2 segundos sin importar el angulo"""
        self.servo_izq.mover(-1)
        self.servo_der.mover(1)
        time.sleep(0.2)
        self.servo_izq.mover(0)
        self.servo_der.mover(0)

    def rotar_der(self):
        """hace una rotacion por 0.2 segundos sin importar el angulo"""
        self.servo_izq.mover(1)
        self.servo_der.mover(-1)
        time.sleep(0.2)
        self.servo_izq.mover(0)
        self.servo_der.mover(0)
