# -*- coding: utf-8 -*-

############################################################
### SERVO V2.2                                           ###
############################################################
### ULTIMA MODIFICACION DOCUMENTADA                      ###
### 18/10/2020                                           ###
### Configuracion de log y uso local                     ###
### Importacion con control de modulo                    ###
### Servos de rotacion continua                          ###
### Chanel 0 por defecto                                 ###
### Creacion                                             ###
############################################################

#Libreria instalada:
#sudo pip3 install adafruit-pca9685

from __future__ import division
import time

try:
    import Adafruit_PCA9685
except:
  print("Modulo Adafrut NO DISPONIBLE")
  No_ADA = True



class Servo(object):
    def __init__(self, channel=0):
        ''' Se puede especificar el numero de servo con channel
            o se puede cambiar luego a travez config
        '''
        # Initialise the PCA9685 using the default address (0x40).
        if not No_ADA:
            self.pwm = Adafruit_PCA9685.PCA9685()
            self.pwm.set_pwm_freq(60)
        # Alternatively specify a different address and/or bus:
        #pwm = Adafruit_PCA9685.PCA9685(address=0x41, busnum=2)
        # datos del servo
        self.max_angle = 180  # Angulo maximo del servo
        self.servo_min = 130  # Min pulse length out of 4096 // depende del servo
        self.servo_mid = 340  # Min pulse length out of 4096 // depende del servo
        self.servo_max = 580  # Max pulse length out of 4096 // depende del servo
        # datos de configuracion
        self.channel    = channel
        self.ang_max    = 180
        self.ang_min    = 0
        self.desp       = 0
        self.invert     = False
        self.ang_actual = 0
        self.log        = self.log_default

    def config(self, channel=0, ang_max=180, ang_min=0, desp=0, invert=False):
        ''' Numero de canal del servo // Numero de servo
            ang_max = Angulo Maximo
            ang_min = Angulo Minino (puede ser negativo)
            desp    = desplazar los angulos para centrar
            invert  = movimiento invertido
        '''
        self.channel = channel
        self.ang_max = ang_max
        self.ang_min = ang_min
        self.desp    = desp
        self.invert = invert
        # mover a la posicion inicial
        self.angulo(0)

    # posibilidad de configurar clase Log(Texto, Modulo)
    def config_log(self, log):
        self.log = log.log

    def config_continuo(self, channel=0, pulso_frenado=301, pulso_max_vel_adelante=401, pulso_max_vel_atras=221, invertir=False):
        ''' Para servos de giro continuo, remplaza el config'''
        self.channel   = channel
        self.servo_min = pulso_max_vel_atras     # Min pulse length out of 4096 // depende del servo
        self.servo_mid = pulso_frenado           # Min pulse length out of 4096 // depende del servo
        self.servo_max = pulso_max_vel_adelante  # Max pulse length out of 4096 // depende del servo
        self.invert    = invertir

    def test_pulso(self, pulso):
        ''' se utiliza para calibrar el minimo y el maximo '''
        self.pwm.set_pwm(self.channel, 0, pulso)

    def check_pulso(self):
        ''' Se utiliza para calibrar el minimo y el maximo con input'''
        print("type EXIT to leave the check")
        pulso = input("PULSO? ")
        while pulso != "EXIT":
            self.test_pulso(int(pulso))
            pulso = input("PULSO? ")
    
    def mover(self, velocidad):
        ''' movimento para servidores continuos
            valores validos 0,1,2,3 - -1,-2,-3
        '''
        pulso = 0
        if self.invert:
            velocidad = velocidad * -1
        if velocidad > 0:
            dif     = self.servo_max - self.servo_mid
            pulso   = int((dif / 3) * velocidad)
        if velocidad < 0:
            dif = self.servo_mid - self.servo_min
            pulso = int((dif / 3) * velocidad)
        if velocidad == 0:
            pulso =  0
        # mover
        pulso_tot =  self.servo_mid + pulso
        # envio de señal
        if not No_ADA:
            self.pwm.set_pwm(self.channel, 0, int(pulso_tot))
        else:
            self.log("MOVER - Channel: " + str(self.channel) + " pulso_tot: " + str(pulso_tot), "SERVO")

    def angulo(self, angle):
        ''' Especificar angulo'''
        # control de angulo max
        if angle > self.ang_max:
           angle = self.ang_max
        # control de angulo min
        if angle < self.ang_min:
           angle = self.ang_min
        # almacenar angulo actual
        self.ang_actual = angle
        #invertir y desplazamos
        if self.invert:
            angle = self.desp - angle  # invertimos el valor
        else:
            angle = self.desp + angle
        # movimiento
        if angle > 90:
           pulso = (((self.servo_max - self.servo_mid) / 90) * (angle-90)) + self.servo_mid
        else:
           pulso = (((self.servo_mid - self.servo_min) / 90) * angle) + self.servo_min
        # envio de señal
        if not No_ADA:
            self.pwm.set_pwm(self.channel, 0, int(pulso))
        else:
            self.log("ANGULO - Channel: " + str(self.channel) + " pulso: " + str(pulso), "SERVO")

    def angulo_actual(self):
        ''' retorna el angulo actual'''
        return self.ang_actual

    # log por defeto
    def log_default(self, texto, modulo):
        print(texto)

