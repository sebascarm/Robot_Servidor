# -*- coding: utf-8 -*-

###########################################################
### TTS V1.2                                            ###
###########################################################
### ULTIMA MODIFICACION DOCUMENTADA                     ###
### 26/02/2020                                          ###
### mejora en la reutilizacion                          ###
### Almacenamiento en folder temporal                   ###
### Reutilizacion de archivos pregrabados               ###
###########################################################


import os
import pygame
from gtts import gTTS


class TTS(object):
    def __init__(self):
        self.speed = 0
        self.tts = ''
        self.tmp_folder = "tmp"
        self.tmp_file = "tmp_sonido.mp3"
        self.log = self.log_default #log por defecto // se puede reemplazar en config
        
    def config(self, Speed=0, Log=''):
        #Opcional funcion log para enviar lo que se dice al log tambien
        self.speed = Speed
        if self.speed == 0:
            pygame.mixer.init()
        else:
            pygame.mixer.init(self.speed)
        if Log != '':
            self.log = Log.log

    def say(self, texto, guardar=True):
        #type: (str, bool)-> None
        """ guardar: opcion para almacenar archivo temporal"""
        if guardar:
            file = texto.replace(" ", "_") + ".mp3"
            #tratamos de cargar el archivo por si existe previamente
            if os.path.isfile(self.tmp_folder + "/" + file):
                self.log("Voz pre-grabada: " + texto, "TTS")
            else:
                self.tts = gTTS(texto, lang='es-us')
                self.tts.save(self.tmp_folder + "/" + file)
            # reproducir
            pygame.mixer.music.load(self.tmp_folder + "/" + file)
        else:
            self.tts = gTTS(texto, lang='es-us')
            self.tts.save(self.tmp_folder + "/" + self.tmp_file)
            pygame.mixer.music.load(self.tmp_folder + "/" + self.tmp_file)

        #envio a Log
        self.log(texto, "TTS")
        pygame.mixer.music.play()
        #Loop mientras esta en sonido
        while pygame.mixer.music.get_busy() == True:
            continue

    def log_default(self, Texto, Modulo):
        print(Texto)