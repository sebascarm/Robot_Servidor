# -*- coding: utf-8 -*-

############################################################
### CLIENTE TCP VERSION 3.0                              ###
############################################################
### ULTIMA MODIFICACION DOCUMENTADA                      ###
### 27/01/2020                                           ###
### Reduccion de codigo                                  ###
### Posibilidad de recibirdatos binarios                 ###
### Espera de 0.1 inecesaria, lectura bloqueante         ###
### Espera de 0.1 para escuchar mensajes entrantes       ###
### timeout en socket para no bloquear proceso al cerrar ###
### Uso de ThreadAdmin                                   ###
### Captura de error al leer datos del puerto            ###
### Evitar intento de conexion conectado                 ###
############################################################

import socket
import time
from thread_admin import ThreadAdmin
import cv2

class Cliente_TCP(object):
    def __init__(self):
        self.soc = ""
        self.conexion       = False             # Estado de la conexion
        self.estado         = 0                 # Valor de utlimo estado
        self.th_conexion    = ThreadAdmin()
        self.th_mensajes    = ThreadAdmin()
        #self.th_recepcion  = ''     # hilo de recepcion
        self.host           = ''
        self.puerto         = ''
        self.buffer         = 1024
        self.callback       = ''
        self.binario        = False

    def config(self, Host, Puerto, Callback, Buffer = 1024, Binario=False):
        self.host       = Host
        self.puerto     = int(Puerto)
        self.buffer     = Buffer
        self.binario    = Binario       # Solo puede recibir binario, envia texto
        self.callback   = Callback      # Funcion de rellamada de estados
        #Mensajes de callback: -1 Error 0 Desconectado 1 Conectando 2 Conectado
        #                       3 Envio de Datos 4 Recepcion de Datos
        #Calback funcion ej: calback(codigo, mensaje): / calback(self, codigo, mensaje): /

    def conectar(self):
        # control de mensajes si ya se encuentra en ejecucion
        if not self.th_cola.state:
            self.th_cola.start(self.__th_mensajes,'','MENSAJES-TCP', 3, self.callback)
        if not self.conexion:
            self.th_conexion.start(self.__th_conectar,'','CONEXION-TCP', 10)
        else:
            self.__estado(-1, "Conexion actualmente establecida")
            

    def __th_conectar(self):
        try:
            self.conexion = True
            self.__estado(1, "Estableciendo conexion")
            self.soc = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.soc.settimeout(3)
            conectar = self.soc.connect((self.host, self.puerto)) #si tiene que usarse
            self.__estado(2, "Conexion establecida")
            self.__recibir()
        except Exception:
            self.conexion = False
            self.__estado(-1, "Error en conexion")

    def enviar(self, mensaje):
        if self.conexion:
            try:
                self.soc.sendall(mensaje.encode('utf-8'))
                self.__estado(3, "Enviado: " + mensaje)
            except:
                self.desconectar()
                self.__estado(-1, "Problemas al enviar datos.  Conexion Cerrada")
        else:
            try:
                self.__estado(-1, "Sin Conexion: " + mensaje)
            except:
                print("Sin Conexion: " + mensaje)

    def __recibir(self):
        self.soc.settimeout(3) #time out de escucha // posiblementa innecesario
        while self.conexion:
            try:
                recibido = self.soc.recv(self.buffer)    #leer del puerto - posible bloqueo hasta recepcion (con timeout no hay)
                if recibido == b'':
                    self.__estado(-1, "Servidor Desconectado")
                    self.desconectar()
                else:
                    self.__estado(4, recibido.decode()) # Recepcion de datos
            except socket.timeout as err:
                pass    # time out continua con el loop
            except Exception as err:
                self.__estado(-1, "Error SOC: " + str(err))
                self.desconectar()
            # Espera antes de leer nuevamente el puerto // elimanda la espera ya que la lectura es bloqueante
            # time.sleep(0.1)

    # recepcion binaria
    def __recibir_bin(self):        
        self.soc.settimeout(3) #time out de escucha // posiblementa innecesario
        payload_size = struct.calcsize("H")
        print (payload_size)
        while self.conexion:
            while len(recibido) < payload_size:
                try:
                    recibido += self.soc.recv(self.buffer)  # leer del puerto - posible bloqueo hasta recepcion (con timeout no hay)
                    if recibido == b'':
                        self.__estado(-1, "Servidor Desconectado")
                        self.desconectar()
                    else:
                        # correcto
                        packed_msg_size = recibido[:payload_size]
                        recibido = recibido[payload_size:]
                        msg_size = struct.unpack("H", packed_msg_size)[0]
                        while len(recibido) < msg_size:
                            recibido += self.soc.recv(self.buffer)  # leer del puerto - posible bloqueo hasta recepcion (con timeout no hay)
                        frame_data = recibido[:msg_size]
                        recibido = recibido[msg_size:]
                        ###
                        frame=pickle.loads(frame_data)
                        print frame
                        cv2.imshow('frame',frame)


                except socket.timeout as err:
                    pass    # time out continua con el loop
                except Exception as err:
                    self.__estado(-1, "Error SOC: " + str(err))
                    self.desconectar()
            

            


        
    def desconectar(self):
        try:
            self.conexion = False
            self.th_conexion.close()
            self.soc.close()
            self.__estado(0, "Conexion Cerrada")
        except Exception:
            self.__estado(-1, "Error al cerrar conexion")

    # codificacion y envio de estados y mensaje
    def __estado(self, Estado, Mensaje):
        self.estado = Estado
        self.cola_codigo.put(Estado)
        self.cola_mensaje.put(Mensaje)

    # loop de lectura de mensajes
    def __th_mensajes(self):
        while self.conexion:
            if self.cola_mensaje.qsize() > 0:
                codigo  = self.cola_codigo.get()
                mensaje = self.cola_mensaje.get()
                self.callback(codigo, mensaje)
            time.sleep(self.mensaje_velocidad)
