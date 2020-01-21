# -*- coding: utf-8 -*-

###########################################################
### Clase FACE DETECT V1.0                              ###
###########################################################
### ULTIMA MODIFICACION DOCUMENTADA                     ###
### 14/01/2020                                          ###
### Eliminacion de imports inecesarios                  ###
### Creacion de clase                                   ###
###########################################################

# import argparse
#import time
from imutils.video import VideoStream
import numpy as np
import imutils
import cv2
from componentes.funciones import Path_Actual

class Face_Detect(object):
    def __init__(self):
        self.resolucion     = (320, 240)
        self.frames         = 10 
        self.prob_min       = 0.4   # probabilidad minima de deteccion
        self.log            = self.__log_default
        self.vs             = ''    # video stream
        self.net            = ''    # red neuronal

    def config(self, Resolucion=(320,240), Frames=10):
        self.resolucion = Resolucion
        self.frames     = Frames
        
    
    def config_log(self, Log):
        #posibilidad de configurar clase Log(Texto, Modulo)
        self.log = Log.log

    def iniciar(self):
        # lectura de modelos de disco
        self.log("Cargando modelo", "FACE_DETECT")
        proto = Path_Actual(__file__) + '/face_detect_files/deploy.prototxt.txt'
        model = Path_Actual(__file__) + '/face_detect_files/res10_300x300_ssd_iter_140000.caffemodel'
        self.net = cv2.dnn.readNetFromCaffe(proto, model)
        # inicializar video
        self.log("Iniciando video stream", "FACE_DETECT")
        self.vs = VideoStream(src=0).start()
        #time.sleep(1.0)
        self.log("Reconocimento iniciado", "FACE_DETECT")
        print("hola")
        # Loop
        while True:
            # Lectura de frame
            frame = self.vs.read()
            frame = imutils.resize(frame, width=800)
            (h, w) = frame.shape[:2]
            # conversion a blob
            blob = cv2.dnn.blobFromImage(cv2.resize(frame, (300, 300)), 1.0,
		        (300, 300), (104.0, 177.0, 123.0))
            # enviar el blob a red neuronal y obtener deteccion
            self.net.setInput(blob)
            detections = self.net.forward()
            # loop sobre las detecciones encntradas
            for i in range(0, detections.shape[2]):
                confidence = detections[0, 0, i, 2]     # extraer la probabilidad
                if confidence < self.prob_min:
                    continue
                # generar cuadro
                box = detections[0, 0, i, 3:7] * np.array([w, h, w, h])
                (startX, startY, endX, endY) = box.astype("int")
                # dibujar recuadro y probabilidad
                text = "{:.2f}%".format(confidence * 100)
                y = startY - 10 if startY - 10 > 10 else startY + 10
                cv2.rectangle(frame, (startX, startY), (endX, endY),(0, 0, 255), 2)
                cv2.putText(frame, text, (startX, y), cv2.FONT_HERSHEY_SIMPLEX, 0.45, (0, 0, 255), 2)
            
            # Mostrar el cuadro final
            cv2.imshow("Frame", frame)
            # Salir con Q
            key = cv2.waitKey(1) & 0xFF
            if key == ord("q"):
                break

    # Log por defecto
    def __log_default(self, Texto, Modulo):
        print(Texto)

    