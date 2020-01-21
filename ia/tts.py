# -*- coding: utf-8 -*-

###########################################################
### TTS V1.1                                            ###
###########################################################
### ULTIMA MODIFICACION DOCUMENTADA                     ###
### 04/01/2020                                          ###
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

    def say(self, Texto, Tmp_file="tmp_sonido.mp3"):
        self.tmp_file = Tmp_file
        if Tmp_file != "tmp_sonido.mp3":
            #tratamos de cargar el archivo por si existe previamente
            if os.path.isfile(self.tmp_folder + "/" + self.tmp_file):
                pygame.mixer.music.load(self.tmp_folder + "/" + self.tmp_file)
                self.log("Voz pre-grabada", "TTS")
            else:
                self.tts = gTTS(Texto, lang='es-us')
                self.tts.save(self.tmp_folder + "/" + self.tmp_file)
                pygame.mixer.music.load(self.tmp_folder + "/" + self.tmp_file)
        else:
            self.tts = gTTS(Texto, lang='es-us')
            self.tts.save(self.tmp_folder + "/" + self.tmp_file)
            pygame.mixer.music.load(self.tmp_folder + "/" + self.tmp_file)

        #envio a Log
        self.log(Texto, "TTS")
        pygame.mixer.music.play()
        #Loop mientras esta en sonido
        while pygame.mixer.music.get_busy() == True:
            continue

    def log_default(self, Texto, Modulo):
        print(Texto)