# -*- coding: utf-8 -*-

############################################################
### CLASE GENERAL N1 COMUNICACION V 1.1                  ###
############################################################
### ULTIMA MODIFICACION DOCUMENTADA                      ###
### 04/01/2020                                           ###
### Se incluye configuracion de Log                      ###
############################################################

# LONG FIJA  | LONG VARIABLE
# 012 456 890 2.......             
# <iD|LON|CHK|MODULO|COMANDO|VALOR> 
# Para comprobar se utiliza el CHK = 000

from componentes.comunic.servidor_tcp import Servidor_TCP
from componentes.funciones import GetChkSum
from componentes.funciones import Val_to_text


class Comunicacion(Servidor_TCP):
    def __init__(self): 
        super().__init__() # instanciamos la clase padre
        self.id_recep = "-1"
        self.id_send  = "00"
        self.long_ini = 13
        self.log = self.log_default
    
    def config(self, Ip= "127.0.0.1", Puerto=50001, Buffer =1024): # Con parametros opcionales
        super().configuracion(self.callback, Ip, Puerto, Buffer)
    
    def config_log(self, Log):
        #posibilidad de configurar clase Log(Texto, Modulo)
        self.log = Log.log

    def iniciar(self):
        super().iniciar()
        self.log("INICIANDO COMUNICACION", "COMUNIC")

    def callback(self, Numero, Mensaje):
        msg = str(Numero) + " " + str(Mensaje)
        self.log(msg, "COMUNIC")

    
    def enviar(self, Modulo, Comando, Valor):
        self.id_send = self.get_id(self.id_send)
        ModComando   = str(Modulo) + "|" + str(Comando) + "|" + str(Valor)
        long         = self.get_long(ModComando)
        chk          = "000" # valor de checksum para obtener el checksum
        texto_chk    = "<" + self.id_send + "|" + long + "|" + chk + "|" + ModComando + ">"
        chk_hash     = Val_to_text(GetChkSum(texto_chk),3)
        texto        = "<" + self.id_send + "|" + long + "|" + chk_hash + "|" + ModComando + ">"
        super().enviar(texto)
    
    def recepcion(self, Mensaje):
        #control hash
        id           = Mensaje[1:3]
        long         = int(Mensaje[4:7])
        chk_hash     = Mensaje[8:11]
        
        texto        = Mensaje[0:7] + "|000|" + Mensaje[12:long]
        print("TEXTO:" + texto)
        chk_hash_cmp = Val_to_text(GetChkSum(texto),3)
        if chk_hash_cmp != chk_hash:    #hash incorrecto
            self.log("HASH ERROR: " + texto + " ESPERADO: " + chk_hash_cmp, "COMUNIC")    
        elif self.id_recep != id:
            if self.id_recep != "-1":
                self.log("ID ERROR: " + texto + " ESPERADO: " + self.id_recep, "COMUNIC")
                self.id_recep = id
                self.id_recep = self.get_id(self.id_recep)
            else:
                #ID INICIAL
                self.id_recep = id
                #incrementar la recepcion
                self.id_recep = self.get_id(self.id_recep)
                self.log("OK INI: "+ texto, "COMUNIC")    
        else:
            #recepcion correcta
            self.log("OK: "+ texto, "COMUNIC")
            #incrementar la recepcion
            self.id_recep = self.get_id(self.id_recep)

    def procesar(self, Mensaje):
        self.log("OK: "+ texto, "COMUNIC")

    #elementos internos
    def get_id(self, id):
        val_id = int(id) 
        val_id +=1
        if (val_id > 99):
            val_id = 0
        return Val_to_text(val_id,2)

    def get_long(self, ModComando):
        long_envio = len(ModComando) + self.long_ini
        return Val_to_text(long_envio,3)


    def log_default(self, Texto, Modulo):
        print(Texto)
    
