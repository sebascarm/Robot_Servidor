# -*- coding: utf-8 -*-

###########################################################
### Clase CAPTURADORA DE CAMARA V1.0                    ###
###########################################################
### ULTIMA MODIFICACION DOCUMENTADA                     ###
### 08/01/2020                                          ###
###########################################################

import pygame
import pygame.camera

from componentes.timer import Timer

class Camara(object):
    def __init__(self):
        self.resolucion     = (320, 240)
        self.frames         = 10    
        self.windows        = False
        self.visible        = False
        self.pantalla       = ''
        self.camara         = ''
        self.captura        = ''
        self.captura_final  = ''
        self.numero_imagen  = 0
        self.pausa          = 100
        self.loop           = True 
        self.log            = self.log_default
        self.visible        = False
        self.conectado      = False
        self.timer          = Timer()
        
        
    def config(self, Resolucion=(320,240), Frames=10, Windows=False, Visible=False):
        self.resolucion = Resolucion
        self.frames     = Frames
        self.windows    = Windows
        self.visible    = Visible

    def config_log(self, Log):
        #posibilidad de configurar clase Log(Texto, Modulo)
        self.log = Log.log

    def iniciar(self):
        self.__inicializar()
        self.__loop()

    def __inicializar(self):
        self.log("Iniciado Camara", "CAMARA")
        #INICIALIZAR CAMARA
        pygame.init()
        pygame.camera.init()
        #Modo Windows o Linux        
        if self.windows:
            self.log("Usando Windows", "CAMARA")
            cameras = pygame.camera.list_cameras()
            self.log("Usando camera %s ..." % cameras[0], "VIDEO")
            #self.camara = pygame.camera.Camera(cameras[0],(640,480),"RGBA")
            self.camara = pygame.camera.Camera(cameras[0],self.resolucion,"RGBA")
        else:
            self.log("Usando Linux", "VIDEO")
            #self.camara = pygame.camera.Camera("/dev/video0", (640,480),"RGBA")
            self.camara = pygame.camera.Camera("/dev/video0", self.resolucion,"RGBA")
        #Iniciamos la camara
        self.camara.start()
        #mostramos en pantalla (si es necesario)
        if self.windows or self.visible:
            self.pantalla = pygame.display.set_mode(self.resolucion, 0)
            #self.captura  = pygame.surface.Surface((640,480), 0, self.pantalla)
            self.captura  = pygame.surface.Surface(self.resolucion, 0, self.pantalla)

    def __loop(self):
        self.log("Iniciado el loop de captura", "CAMARA")
        numero_imagen = 0
        self.timer.iniciar()
        while self.loop:
            self.__Capturar()
            self.__Almacenar()
            self.__Visualizar()
            self.__Interrupcion()
            
            delay = self.timer.delay(self.frames)
            pygame.time.delay(delay)
            tiempo = self.timer.fps()
            self.timer.iniciar()
            #print ("fps", tiempo)

    def __Capturar(self):
        # Si no esta conectado o no es visible no tiene sentido capturar
        if (self.conectado) or (self.visible):
            if self.windows:
                self.captura = self.camara.get_image(self.captura)
            else:
                # En linux podemos capturar la imagen sin un visualizador
                self.captura = self.camara.get_image()
                pass
            # Corregir en futuro si va a ser necesario la transformacion
            self.captura_final = pygame.transform.scale(self.captura, self.resolucion)
            
    def __Almacenar(self):
        # Grabamos imagenes si hay conexion
        if self.conectado == 1:
            nombre_imagen = "imagenes_tmp/img_tmp" + str(self.numero_imagen) + ".jpg"
            pygame.image.save(self.captura_final, nombre_imagen)
            #imagen guardada (incrementamos el contador)
            self.numero_imagen += 1
            if self.numero_imagen == 10:
                self.numero_imagen = 0
            
    def __Visualizar(self):
        # Mostramos imagen si esta visible
        if self.visible:
           self.pantalla.blit(self.captura_final ,(0,0))
           pygame.display.update()
    
    def __Interrupcion(self):
        # Interupcion
        if self.windows or self.visible:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.camara.stop()
                    pygame.quit()
                    self.loop = False
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        self.camara.stop()
                        pygame.quit()
                        self.loop = False
    
    
    def log_default(self, Texto, Modulo):
        print(Texto)
      