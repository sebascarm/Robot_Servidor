# -*- coding: utf-8 -*-

###########################################################
### Clase FACE DETECT V2.1                              ###
###########################################################
### ULTIMA MODIFICACION DOCUMENTADA                     ###
### 21/01/2020                                          ###
### Utilizacion de clase propia webcam                  ###
### Funcion unica devuelve angulo unico                 ###
### Clase con Procesos                                  ###
### Funciones callback                                  ###
### Eliminacion de imports inecesarios                  ###
### Creacion de clase                                   ###
###########################################################

# import argparse
import time
#from imutils.video import VideoStream
import numpy as np
import imutils
import cv2
from componentes.funciones import Path_Actual
from componentes.thread_admin import ThreadAdmin
from componentes.webcam import Webcam

import array as arr

class Face_Detect(object):
    def __init__(self):
        self.resolucion     = (320, 240)
        self.frames         = 10 
        self.prob_min       = 0.5   # probabilidad minima de deteccion
        self.log            = self.__log_default
        self.cv             = cv2
        self.vs             = Webcam()  # webcam
        self.net            = ''    # red neuronal
        self.frame          = ''    # imagen capturada      
        self.frameshow      = None  # imagen a mostrar
        self.ancho          = 0
        self.alto           = 0
        self.th_detect      = ThreadAdmin()
        self.th_show        = ThreadAdmin()
        self.activo         = False # Estado de ejecucion
        #
        self.show          = False # Para visualizar o no (Tests)   
        self.func_detect   = ''  # llama la funcion con deteccion 
        self.func_cuadro   = ''  # retorna coordenadas de cuadro rostro
        self.func_vista    = ''  # retorna punto de vista de rostro
        self.func_cent_vis = ''  # funcion q retorna valores para centrar la vista
        self.func_unica    = ''  # funcion q retorna valor unico de angulo de centrado de vista (tomando rangos de min y max) 
        #
        self.ang_x         = 0   # ultimo angulo 
        self.ang_y         = 0   # ultimo angulo 
        self.min_x         = 4  # valor diferencia minimo para funcion unica 
        self.min_y         = 4  # valor diferencia minimo para funcion unica 
        self.x             = 0 
        self.y             = 0  
        self.elementos     = [] 
        
                
    def config(self, Resolucion=(320,240), Frames=10, Show=False):
        self.resolucion = Resolucion
        self.frames     = Frames
        self.show       = Show
        #
        proto = Path_Actual(__file__) + '/face_detect_files/deploy.prototxt.txt'
        model = Path_Actual(__file__) + '/face_detect_files/res10_300x300_ssd_iter_140000.caffemodel'
        self.net = self.cv.dnn.readNetFromCaffe(proto, model)
        #
        #self.vs.config()
        
        if self.show:
            self.log("Iniciando video show", "FACE_DETECT")   
            self.th_show.start(self.__th_show,'','FACE_SHOW', callback=self.__callaback_th)    

    def config_callback(self, Func_Detect='', Func_Cuadro='', Func_Vista='', Func_Cent_Vista='', Func_Unica=''):
        # Func_Detect = Funcion()
        # Func_Cuadro = Funcion(X,Y,Ancho,Alto)
        # Func_Vista  = Funcion(X,Y)
        # Func_Cent_Vista = Funcion(X,Y)
        # Func_Unica      = Funcion(X,Y)
        self.func_detect = Func_Detect
        self.func_cuadro = Func_Cuadro    
        self.func_vista  = Func_Vista
        self.func_cent_vis = Func_Cent_Vista
        self.func_unica  = Func_Unica
        
        
    def config_log(self, Log):
        #posibilidad de configurar clase Log(Texto, Modulo)
        self.log = Log.log
        self.vs.config_log(Log)

    def check(self, source=0):
        return self.vs.check()

    def iniciar(self):
        # inicializar video
        self.vs.start() 
        self.activo = True
        self.log("Iniciando video stream", "FACE_DETECT")
        self.th_detect.start(self.__th_loop,'','FACE_DETECT', callback=self.__callaback_th)
        
    def stop(self):
        self.activo = False
    
    def __th_show(self):
        while True:
            if (self.frameshow is not None):
                time.sleep(0.01)
                self.cv.imshow("Frame", self.frameshow)
                ## Salir con Q
                key = self.cv.waitKey(1) & 0xFF
                if key == ord("q"):
                    break 


    def __th_loop(self):
        self.log("Loop de deteccion", "FACE_DETECT")
        # Loop
        while self.activo:
            # Lectura de frame
            self.frame = self.vs.read()
            # Ajuste de tamaño
            self.frame = imutils.resize(self.frame, width=self.resolucion[0], height=self.resolucion[1])
            #h y w devuelve la resolucion real
            (self.alto, self.ancho) = self.frame.shape[:2]
            # conversion a blob en 300 x 300
            blob = self.cv.dnn.blobFromImage(self.cv.resize(self.frame, (300, 300)), 1.0,(300, 300), (104.0, 177.0, 123.0))
            # enviar el blob a la red neuronal y obtener deteccion
            self.net.setInput(blob)
            detections = self.net.forward()
            # loop sobre las detecciones encntradas
            for i in range(0, detections.shape[2]):
                confidence = detections[0, 0, i, 2]     # extraer la probabilidad
                if confidence > self.prob_min:
                    # detectado
                    self.__deteccion(detections, i)
            # revisamos si es vista unica una vez q reviso todo
            if self.func_unica != '':
                #pass
                self.__funcion_unica()
            
            #dibujamos
            self.frameshow = self.frame
        
        #fin de streaming
        self.vs.stop()
        
    
    def __funcion_unica(self):
        if self.elementos:
            maximos = max(self.elementos)
            self.elementos.clear()
            # contruir
            x = maximos[1]
            y = maximos[2]
            box = maximos[3]
            xc = maximos[4]
            yc = maximos[5]
            # determinar angulo de desplazamiento (30 es el grado focal de la camara)
            angulo_x = int((xc / (self.resolucion[0]/2)) * 30)
            angulo_y = int((yc / (self.resolucion[1]/2)) * 30)
            if (abs(angulo_x) > self.min_x) or (abs(angulo_y) > self.min_y):
                if (self.ang_x != angulo_x) or (self.ang_y != angulo_y):
                    self.func_unica(angulo_x,angulo_y)
                    self.ang_x = angulo_x
                    self.ang_y = angulo_y
            else:
                if (self.ang_x != 0) or (self.ang_y != 0):
                    self.func_unica(0, 0)
                    self.ang_x = 0
                    self.ang_y = 0
            # dibuja rectangulo
            if (self.show):
                (startX, startY, endX, endY) = box.astype("int")
                self.cv.rectangle(self.frame, (startX, startY), (endX, endY),(0, 0, 255), 2)
                # dibujar el centro de vista
                self.cv.circle(self.frame,(x,y),10,(0,0,255), 2)
        

    def __deteccion(self, detections, elemento):
        # envelementoar detectado
        if self.func_detect != '':
            # llamar funcion
            self.func_detect()
        # enviar cuadro o vista
        if (self.func_cuadro != '') or (self.func_vista != '') or (self.func_cent_vis != '') or ((self.func_unica != '')):
            #generar coordenadas al rededor del rostro 
            box = detections[0, 0, elemento, 3:7] * np.array([self.ancho, self.alto, self.ancho, self.alto])
            (startX, startY, endX, endY) = box.astype("int")
            y = startY - 10 if startY - 10 > 10 else startY + 10
            # devolvemos la funcion cuadro
            if (self.func_cuadro != ''):
                self.func_cuadro(startX, startY, endX, endY)
            # calculamos la funcion vista
            if (self.func_vista != '') or ((self.func_cent_vis != '')) or ((self.func_unica != '')) :
                x = int(startX + ((endX - startX)/2))
                y = int(startY + ((endY - startY)/3))
                # devolvemos la funcion vista
                if (self.func_vista != ''):
                    self.func_vista(x, y)
                if (self.func_cent_vis != '') or (self.func_unica != ''):
                    xc = x - (self.ancho/2)
                    yc = y - (self.alto/2)
                    # devolvemos la funcion centrado
                    if (self.func_cent_vis != ''):
                        self.func_cent_vis(xc,yc)
                # identificar un unico rostro
                if (self.func_unica != ''):
                    taman = (box[2] - box[0]) * (box[3] - box[1])
                    #self.elementos[elemento] = taman
                    resul = [taman, x, y, box, xc, yc]
                    self.elementos.append(resul)
            # solo si no esta la funcion unica        
            if (self.show) and (self.func_unica == ''):
                # dibuja rectangulo
                if self.func_cuadro != '':
                    self.cv.rectangle(self.frame, (startX, startY), (endX, endY),(0, 0, 255), 2)
                # dibujar el centro de vista
                if self.func_vista != '':
                    self.cv.circle(self.frame,(x,y),10,(0,0,255), 2)
                

    # Log por defecto
    def __log_default(self, Texto, Modulo):
        print(Texto)

    def __callaback_th(self, Codigo, Mensaje):
        self.log(Mensaje, "FACE_DETECT")

    