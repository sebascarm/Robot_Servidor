# -*- coding: utf-8 -*-

###########################################################
### ROBOT CARA V1.0                                     ###
###########################################################
### ULTIMA MODIFICACION DOCUMENTADA                     ###
### 26/02/2020                                          ###
### Creacion                                            ###
###########################################################

from sensores.servo import Servo
from compuesto.robot_cuerp import Robot_Cuerpo

class Robot_Cara(object):
    def __init__(self):
        self.servo_x = Servo()
        self.servo_y = Servo()
        # cuerpo
        self.cuerpo = '' # type: Robot_Cuerpo


    def config(self):
        self.servo_x.config(channel=1, ang_max=70, ang_min=-70, desp=85)
        self.servo_y.config(channel=2, ang_max=25, ang_min=0, desp=95, invert=True)

    def config_cuerpo(self, cuerpo):
        # type: (Robot_Cuerpo)->None
        """ Configurar los elementos del cuerpo
            rueda izquirda y derecha
        """
        self.cuerpo = cuerpo

    def mover(self, ang_x=0, ang_y=0):
        ''' desplaza los angulos expresados con respecto a la posicion actual
        '''
        # movimiento en X
        if ang_x != 0:
            ang_actual = self.servo_x.angulo_actual()
            ang_nuevo  = ang_actual + int(ang_x)
            # revisamos si no superamos los angulos para mover el cuerpo
            print("ANG NUEVO: ", ang_nuevo)
            if ang_nuevo > self.servo_x.ang_max:
                print("ROTAR IZQUIERDA")
                self.cuerpo.rotar_izq()
            elif ang_nuevo < self.servo_x.ang_min:
                print("ROTAR DERECHA")
                self.cuerpo.rotar_der()
            # desplazar camara
            else:
                self.servo_x.angulo(ang_nuevo)

        # movimiento en Y
        if ang_y != 0:
            ang_actual = self.servo_y.angulo_actual()
            ang_nuevo = ang_actual + int(ang_y)
            # desplazar
            self.servo_y.angulo(ang_nuevo)