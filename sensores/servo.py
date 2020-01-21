# -*- coding: utf-8 -*-

############################################################
### SERVO V 1.0                                          ###
############################################################
### ULTIMA MODIFICACION DOCUMENTADA                      ###
### 21/01/2020                                           ###
### Creacion                                             ###
############################################################

#Libreria instalada:
#sudo pip3 install adafruit-pca9685

from __future__ import division
import time
import Adafruit_PCA9685

class Servo(object):
    def __init__(self, channel):
        # Initialise the PCA9685 using the default address (0x40).
        self.pwm = Adafruit_PCA9685.PCA9685()
        # Alternatively specify a different address and/or bus:
        #pwm = Adafruit_PCA9685.PCA9685(address=0x41, busnum=2)
        self.pwm.set_pwm_freq(60)
        #
        self.max_angle = 180  # Angulo maximo del servo
        self.servo_min = 130  # Min pulse length out of 4096 // depende del servo
        self.servo_mid = 340  # Min pulse length out of 4096 // depende del servo
        self.servo_max = 580  # Max pulse length out of 4096 // depende del servo
        #
        self.channel   = 0

    def config(self, Channel):
        # Numero de canal del servo // Numero de servo
        self.channel = Channel

    def test_pulso(self, pulso):
        #se utiliza para calibrar el minimo y el maximo
        self.pwm.set_pwm(self.channel, 0, pulso)

    def check_pulso(self):
        #se utiliza para calibrar el minimo y el maximo con input
        print("type EXIT to leave the check")
        pulso = input("PULSO? ")
        while pulso != "EXIT":
            self.test_pulso(int(pulso))
            pulso = input("PULSO? ")
    
    def angulo(self, angle):
       if angle > 90:
           pulso = (((self.servo_max - self.servo_mid) / 90) * (angle-90)) + self.servo_mid
       else:
           pulso = (((self.servo_mid - self.servo_min) / 90) * angle) + self.servo_min
       self.pwm.set_pwm(self.channel, 0, int(pulso)) 
