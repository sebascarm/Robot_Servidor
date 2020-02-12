# -*- coding: utf-8 -*-

############################################################
### SERVIDOR TCP VERSION 3.6                             ###
############################################################
### ULTIMA MODIFICACION DOCUMENTADA                      ###
### 04/02/2020                                           ###
### Correcion en salida de thread en espera de conexion  ###
### Uso de nuevo Thread con salida                       ###
### Correcion en cierre de conexion y otros              ###
### Reduccion de codigo                                  ###
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

import pickle  # para envio de binarios
import struct  # para envio de binarios


class Servidor_TCP(object):
    def __init__(self):
        # Variable local de conexion
        self.conexion = False  # Estado de la conexion
        self.estado = 0  # Valor de utlimo estado
        self.salir = False  # Variable de salida
        # self.cola_recepcion = queue.Queue()     # Cola de datos # no usada al momento
        self.cola_codigo = queue.Queue()  # Cola de devolucion de codigo
        self.cola_mensaje = queue.Queue()  # Cola de devolucion de detalle del codigo
        self.mensaje_velocidad = 0.001  # delay en ms entre el loop de mensajes
        self.conexiones = 1  # Cantidad de conexiones admitidas
        self.sc = ''  # Socket
        self.sock = ''  # Socket
        # variables de configuracion
        self.ip = ''
        self.puerto = ''
        self.tam_buffer = ''  # el tamano se usa para la recepcion
        self.binario = False  # utilizado para enviar imagenes // se debe cambiar el tamaño del buffer

        self.th_conexion = ThreadAdmin()
        self.th_cola = ThreadAdmin()
        self.reintento = 50
        self.binario = False  # para enviar datos binarios

    def config(self, Host="127.0.0.1", Puerto=50001, Buffer=1024, Callback='',
               Binario=False):  # Con parametros opcionales
        self.ip = Host
        self.puerto = Puerto
        self.tam_buffer = Buffer
        self.binario = Binario  # utilizado para enviar imagenes // solo envia binario - no recibe
        self.callback = Callback  # Funcion de rellamada de estados
        # Mensajes de callback: 0 Desconectado| 1 Conectando| 2 Conectado
        # 3 Envio de datos| 4 Recepcion de datos|-1 Error

    def iniciar(self):
        # control de mensajes si ya se encuentra en ejecucion
        if not self.th_cola.state:
            self.th_cola.start(self.__th_mensajes, '', 'MENSAJES-TCP', 3, self.__callaback_th, True)
        # inicio de intento de escucha
        if not self.conexion:
            self.th_conexion.start(self.__th_reintento_escucha, '', 'SERV-TCP', 3, self.__callaback_th, True)
        else:
            self.__estado(-1, "Conexion actualmente establecida")

    # Servidor (re-intentos de escucha de conexiones)
    def __th_reintento_escucha(self, run):
        if not self.conexion:
            intento = 0
            while (intento < self.reintento) and run.value:
                self.__intento_conexion(run)
                if self.estado == -1:
                    intento += 1  # no pudo conectarse
                if self.estado == 2:
                    self.__interno_escuchar(run)  # conecto pasamos a escuchar y liberamos los reintentos
                    intento = 0
                    # en cuanto se corta la conexion vuelve a este loop para los reintentos de conexion
                time.sleep(5)  # espera de 5 segundos antes de reintentar conexion

    # Servidor (intento de conexion)
    def __intento_conexion(self, run):
        # INTENTO DE CONEXION
        try:
            self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.sock.settimeout(3)  # timeout de conexion
            self.sock.bind((self.ip, self.puerto))
            self.sock.listen(self.conexiones)
            self.__estado(1, "Esperando conexion remota en: " + str(self.ip) + " " + str(self.puerto))
        except:
            self.__estado(-1, "No es posible asignar el puerto: " + str(self.ip) + " " + str(self.puerto))

        # BLOQUE DE ESPERA DE CONEXION
        while self.estado == 1 and run.value:
            try:
                self.sc, addr = self.sock.accept()  # Bloquea hasta que se conectan o por timeout
                self.conexion = True
                self.__estado(2, "Conexion establecida")
            except socket.timeout as err:
                pass  # time out continua con el loop
            except Exception as err:
                self.conexion = False
                self.__estado(-1, "Error SOC: " + str(err))

    # loop de escucha de mensajes una vez establecida la conexion
    def __interno_escuchar(self, run):
        # LOOP DE ESCUCHA
        recibido = ""
        self.sc.settimeout(3)  # time out de escucha
        while self.conexion and run.value:
            try:
                recibido = self.sc.recv(self.tam_buffer)  # leer del puerto - posible bloqueo hasta recepcion
                if recibido == b'':
                    self.desconectar()
                    self.__estado(0, "Cliente Desconectado - Reception end")
                else:
                    self.__estado(4, recibido.decode())  # Recepcion CORRECTA de datos
            except socket.timeout as err:
                pass  # time out continua con el loop
            except:
                self.desconectar()
                self.__estado(0, "Cliente Desconectado - Reception error")
        # antes de salir cerrar para liberar puertos

    def enviar(self, mensaje):
        if self.conexion:
            try:
                if self.binario:  # datos binarios // ej: imagenes
                    datos = pickle.dumps(mensaje)  # para datos binarios (serializacion de datos)
                    # Send message length first
                    message_size = struct.pack("Q", len(datos))  # tamaño "Q" 8 bytes
                    # envio
                    self.sc.sendall(message_size + datos)
                    # Envio de info local
                    self.__estado(3, "SEND: DATOS BINARIOS")
                else:
                    datos = str(mensaje)
                    self.sc.sendall(datos.encode('utf-8'))
                    # Envio de info local
                    self.__estado(3, "SEND: " + datos)
            except:
                self.desconectar()
                self.__estado(-1, "Problemas al enviar datos - Conexion Cerrada")

    def desconectar(self):
        if self.conexion:
            self.sc.close()
            self.sock.close()
        self.estado = 0
        self.conexion = False
        self.__estado(0, "Conexion Cerrada")

    # codificacion y envio de estados y mensaje
    def __estado(self, Estado, Mensaje):
        self.estado = Estado
        self.cola_codigo.put(Estado)
        self.cola_mensaje.put(Mensaje)

    # loop de lectura de mensajes
    def __th_mensajes(self, run):
        # while self.conexion:
        while run.value:
            if self.cola_mensaje.qsize() > 0:
                codigo = self.cola_codigo.get()
                mensaje = self.cola_mensaje.get()
                self.callback(codigo, mensaje)
            time.sleep(self.mensaje_velocidad)

    # Callback de TH
    def __callaback_th(self, Codigo, Mensaje):
        print(Mensaje)
