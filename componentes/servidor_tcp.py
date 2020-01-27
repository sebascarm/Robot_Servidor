# -*- coding: utf-8 -*-

############################################################
### SERVIDOR TCP VERSION 3.0                             ###
############################################################
### ULTIMA MODIFICACION DOCUMENTADA                      ###
### 27/01/2020                                           ###
### Posibilidad de enviar datos binarios                 ###
### Se cambia la ubicacion del ThreadAdmin               ###
### Timeout en escucha para poder cerrar sin bloquear(3s)###
### (Ante desconexion por error el mensaje sigue activo) ###
### Uso de colas en mensajes y reintento de conexion     ###
### Uso de log en thread                                 ###
### Timeout en espera de conexion                        ###
############################################################

import socket
import queue
import time
from componentes.thread_admin import ThreadAdmin

class Servidor_TCP(object):
    def __init__(self): 
        #Variable local de conexion
        self.conexion       = False             # Estado de la conexion
        self.estado         = 0                 # Valor de utlimo estado
        self.salir          = False             # Variable de salida
        self.cola_recepcion = queue.Queue()     # Cola de datos # no usada al momento
        self.cola_codigo    = queue.Queue()
        self.cola_mensaje   = queue.Queue()
        self.conexiones     = 1
        self.sc = ""
        self.th_conexion    = ''
        self.th_cola        = ThreadAdmin()
        self.reintento      = 50
        self.sin_ejecucion  = False
        self.binario        = False # para enviar datos binarios
                    
    def configuracion(self, Callback, Ip= "127.0.0.1", Puerto=50001, Buffer =1024, Binario=False): # Con parametros opcionales
        self.Ip = Ip
        self.Puerto = Puerto
        self.tam_buffer = Buffer
        self.callback = Callback  #Funcion de rellamada de estados
        #Mensajes de callback: 0 Desconectado| 1 Conectando| 2 Conectado
        # 3 Envio de datos| 4 Recepcion de datos|-1 Error
        self.binario = Binario # utilizado para enviar imagenes // se debe cambiar el tamaño del buffer

    def iniciar(self):
        #self.sin_ejecucion  = False
        # control de mensajes
        if not self.th_cola.state:
            self.th_cola.start(self.__th_mensajes,'','MENSAJES', 3, self.callback)
        self.th_conexion = ThreadAdmin(self.__th_inicio,'','CONEXION',10, self.callback)
        self.sin_ejecucion  = False
    
    def __th_inicio(self):
        if not self.conexion: 
            intento = 0
            while intento < self.reintento:
                self.__interno_conexion()
                time.sleep(5)
                if self.estado == -1:
                    #no pudo conectarse
                    intento += 1
                if self.estado == 2:
                    #conecto pasamos a escuchar y liberamos los reintentos
                    intento = self.reintento
                    self.__interno_escuchar()
                    if not self.th_conexion:
                        self.sin_ejecucion  = True
       
    def __interno_conexion(self):
        # INTENTO DE CONEXION
        try:
            self.estado = 1
            self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.sock.settimeout(5) #timeout de conexion
            self.sock.bind((self.Ip, self.Puerto))
            self.sock.listen(self.conexiones)
            self.cola_codigo.put(self.estado)
            self.cola_mensaje.put("Esperando conexion remota en: " + str(self.Ip) + " " + str(self.Puerto))
        except:
            self.estado = -1
            self.cola_codigo.put(self.estado)
            self.cola_mensaje.put("No es posible asignar el puerto: " +str(self.Ip) + " " + str(self.Puerto))    
        #BLOQUE DE ESPERA DE CONEXION
        while self.estado == 1:
            try:
                self.sc, addr = self.sock.accept()  #Bloquea hasta que se conectan o por timeout
                self.estado   = 2
                self.conexion = True
                self.cola_codigo.put(self.estado)
                self.cola_mensaje.put("Conexion establecida")
            except socket.timeout as err:
                pass    # time out continua con el loop
            except Exception as err:
                self.estado   = -1
                self.conexion = False
                self.cola_codigo.put(self.estado)
                self.cola_mensaje.put("Error SOC: " + str(err))
    
    def __interno_escuchar(self):
        #LOOP DE ESCUCHA 
        recibido = ""
        self.sc.settimeout(3) #time out de escucha
        while self.conexion:
            try:
                recibido = self.sc.recv(self.tam_buffer)    #leer del puerto - posible bloqueo hasta recepcion
                if recibido == b'':
                    self.desconectar()
                    self.estado = 0
                    self.cola_codigo.put(self.estado)
                    self.cola_mensaje.put("Cliente Desconectado - Reception end")
                else:
                    #Recepcion de datos
                    self.estado = 4
                    self.cola_codigo.put(self.estado)
                    self.cola_mensaje.put(recibido.decode())
                    #self.callback(recibido.decode())
            except socket.timeout as err:
                pass    # time out continua con el loop
            except:
                self.desconectar()
                self.estado = 0
                self.cola_codigo.put(self.estado)
                self.cola_mensaje.put("Cliente Desconectado - Reception error")
        #antes de salir cerrar para liberar puertos

    def enviar(self, mensaje):
        if self.conexion:
            try:
                if self.binario: # datos binarios // ej: imagenes
                    datos = pickle.dumps(mensaje) # para datos binarios
                    self.sc.sendall(struct.pack("H", len(datos))+datos) # tal vez cambiar a L // Large
                    # Envio de info local
                    self.estado = 3
                    self.cola_codigo.put(self.estado)
                    self.cola_mensaje.put("SEND: DATOS BINARIOS")
                else:
                    datos = str(mensaje)
                    self.sc.sendall(datos.encode('utf-8'))
                    # Envio de info local
                    self.estado = 3
                    self.cola_codigo.put(self.estado)
                    self.cola_mensaje.put("SEND: " + datos)
            except:
                self.desconectar()
                self.estado = -1
                self.cola_codigo.put(self.estado)
                self.cola_mensaje.put("Problemas al enviar datos - Conexion Cerrada")

    def desconectar(self):
        self.sc.close()
        self.sock.close()
        self.estado   = 0  
        self.conexion = False

    def __th_mensajes(self):
        while not self.sin_ejecucion:
            if self.cola_mensaje.qsize() > 0:
                codigo  = self.cola_codigo.get()
                mensaje = self.cola_mensaje.get()
                self.callback(codigo, mensaje)
            time.sleep(0.1)

