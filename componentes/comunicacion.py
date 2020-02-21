# -*- coding: utf-8 -*-

###########################################################
### COMUNICACION TCP VERSION 3.9                        ###
###########################################################
### ULTIMA MODIFICACION DOCUMENTADA                     ###
### 20/02/2020                                          ###
### Log default                                         ###
### Desconexion                                         ###
### incorporacion de log                                ###
### Correccion solo en alineacion de textos             ###
### Se corrige para el envio binario                    ###
### Se agrega el estado de la conexion                  ###
### correcciones varias                                 ###
### Se envia y recibe paquetes de control               ###
### Objeto aplicable a cliente y servidor               ###
### Correccion en funcion recursiva                     ###
### Encargado de controlar los paquetes TCP             ###
###########################################################

# LONG FIJA  | LONG VARIABLE
# 012 456 890 2.......
# <ID|LON|CHK|MODULO|COMANDO|VALOR>
# Para comprobar se utiliza el CHK = 000
# PAra datos binarios no aplica formato por el momento
# Paquete inicial id = 00
# MODULO|COMANDO|VALOR = no se entrega en esta etapa, se devuelve tode el paquete

from componentes.comunic.cliente_tcp import Cliente_TCP
from componentes.comunic.servidor_tcp import Servidor_TCP
from componentes.funciones import GetChkSum
from componentes.funciones import Val_to_text


class Comunicacion:
    def __init__(self):
        """ Verificamos el estado de la conexion a travez de self.conexion"""
        self.conexion = False   # estado de la conexion
        self.cliente = True     # valor de cliente o servidor
        self.binario = False    # Tipo de datos a utilizar
        self.serv_tcp = ''      # Servidor TCP
        self.cli_tcp = ''       # Cliente TCP
        self.id_recep = -1
        self.id_send = -1
        self.long_recep = "000"
        self.chk_reecp = "000"
        self.long_fija = 13
        self.log = self.__log_default
        self.buffer = 1024      # valor por defecto
        self.call_conex = ''    # Callback de conexion
        self.call_mensaje = ''  # Callback de mensajes
        ## config packet
        self.inicio = "<"
        self.fin = ">"
        self.max_size = 100
        # tipos de busqueda interna
        self.buscar_ini = True
        self.buscar_fin = False
        self.paquete = ''  # paquete de datos completos

    def config(self, ip="127.0.0.1", puerto=50001, cliente=True, binario=False,
               callback=''):  # Con parametros opcionales
        """ Cliente: Especifica si es cliente o servidor TCP
            Binario: Especifica si se trata de datos binarios
            Callback(Codigo, Mensaje) - Retorno de mensajes de conexion
        """
        self.cliente = cliente
        self.call_conex = callback
        self.binario = binario
        if cliente:
            self.cli_tcp = Cliente_TCP()
            self.cli_tcp.config(ip, puerto, self.__call_conex, 1024, binario)
        else:
            self.serv_tcp = Servidor_TCP()
            self.serv_tcp.config(ip, puerto, 1024, self.__call_conex, binario)

    def config_log(self, Log):
        '''posibilidad de configurar clase Log(Texto, Modulo)'''
        self.log = Log.log

    def config_packet(self, inicio="<", fin=">", max_size=100):
        """inicio   = caracter que define el inicio del paquete
           fin      = caracter que define el final del paquete
           max_size = tamaño maximo para buscar el fin del paquete"""
        self.inicio = inicio
        self.fin = fin
        self.max_size = max_size

    def iniciar(self):
        """En caso de ser servidor inicia la escucha, y en caso de ser cliente intenta establecer la conexion"""
        if self.cliente:
            self.cli_tcp.conectar()
        else:
            self.serv_tcp.iniciar()

    def desconectar(self):
        """ Cierre de conexion """
        if self.cliente:
            self.cli_tcp.desconectar()
        else:
            self.serv_tcp.desconectar()

    def enviar(self, mensaje):
        """ envia el mensaje establecido agregando:
            <ID|LON|CHK|-------MENSAJE-------->
        """
        if (not self.cliente) and self.binario: # Si es Servidor Binario no envia de este modo
            self.serv_tcp.enviar(mensaje)
        else:
            self.id_send = get_id(self.id_send)
            id_send = Val_to_text(self.id_send, 2)
            long = len(mensaje) + 13
            chk = "000"  # valor de checksum para obtener el checksum
            texto_chk = self.inicio + id_send + "|" + str(long) + "|" + chk + "|" + mensaje + self.fin
            chk_hash = Val_to_text(GetChkSum(texto_chk), 3)
            texto = self.inicio + id_send + "|" + str(long) + "|" + chk_hash + "|" + mensaje + self.fin
            if self.cliente:
                self.cli_tcp.enviar(texto)
            else:
                self.serv_tcp.enviar(texto)

    # Retornos de conexion
    def __call_conex(self, codigo, mensaje):
        if codigo == 0:
            self.conexion = False
        if codigo == 2:
            self.conexion = True
        if codigo == 4:
            # solo si es servidor o si es cliente no binario
            # el servidor no recibe datos binarios
            if (not self.cliente) or (not self.binario):
                paquete = self.__contro_ini_fin(mensaje)
                while paquete != '':
                    # controlamos el  checksum
                    if self.control_checksum(paquete):
                        # correcto
                        # controlamos la secuencia, por el momento no hacemos nada si es incorrecta, solo enviamos mensaje
                        self.__contro_secuencia(paquete)
                        self.call_conex(4, paquete[10:])  # enviamos el paquete sin la longitud fija
                    else:
                        # checksum error
                        self.call_conex(-2, "Checksum incorrecto")
                    # re llamamos a la funcion de control por si tenemos mas de un paquete en el mismo mensaje
                    paquete = self.__contro_ini_fin('')
            else:
                # recepcion de datos binarios, se envian los datos sin procesar
                self.call_conex(4, mensaje)  # enviamos el paquete sin analisis
        else:
            # codigo distinto a 4
            self.call_conex(codigo, mensaje)

    ###########################################################
    ### CONTROL DE CHECKSUM                                 ###
    ###########################################################
    def control_checksum(self, mensaje):
        chk_reecp = mensaje[6:9]
        # control de checksum
        checksum = GetChkSum(self.inicio + mensaje[0:5] + "|000|" + mensaje[10:] + self.fin)
        if chk_reecp != Val_to_text(checksum, 3):
            return False
        else:
            return True

    ###########################################################
    ### CONTROL DE SECUENCIA                                ###
    ###########################################################
    def __contro_secuencia(self, mensaje):
        id_recep = mensaje[:2]
        id_esperado = get_id(self.id_recep)
        if int(id_recep) == id_esperado:
            # rececpcion correcta
            self.id_recep = id_esperado
            return True
        else:
            if (self.id_recep == -1) and (id_recep == "00"):
                # recepcion de paquete inicial
                self.id_recep = 1
                return True
            else:
                # recepcion secuencia incorrecta
                self.call_conex(-2, "Secuencia incorrecta - recibido: " + id_recep + " esperado: " + Val_to_text(
                    id_esperado, 2) + " Mensaje: " + mensaje)
                self.id_recep = int(id_recep)
                return False

    ###########################################################
    ### CONTROL DE INICIO Y FIN DEL PAQUETE                 ###
    ###########################################################
    def __contro_ini_fin(self, mensaje):
        """Se verifica que se encuentre el inicio y el final con la longitud correcta
           Revisa paquetes desfazados y combina paquetes incompletos
           Devuelve '' cuando surge un error
        """
        pos_ini = 0
        self.paquete += mensaje  # analizamos el mensaje
        if self.paquete == '':
            return ''
        else:
            if self.buscar_ini:
                # Revisamos el inicio del paquete
                if self.paquete[:1] != self.inicio:
                    # buscamos el inicio del paquete
                    pos_ini = self.paquete.find(self.inicio)
                    if pos_ini == -1:
                        # no se encontro el inicio, descartamos los datos actuales
                        # el inicio se puede encontrar en el resto del paquete
                        self.call_conex(-2, "Inicio no encontrado - Perdida de datos")
                        self.paquete = ''
                        return ''
                    else:
                        # inicio encontrado, pero desfazado, eliminar parte inicial del paquete
                        self.call_conex(-2, "Inicio desplazado - Perdida de datos")
                        self.paquete = self.paquete[pos_ini:]
                        self.buscar_ini = False
                        self.buscar_fin = True
                        return ''
                else:
                    # el inicio es correcto
                    self.buscar_ini = False
                    self.buscar_fin = True

            if self.buscar_fin:
                # busqueda de fin de paquete
                pos_fin = self.paquete.find(self.fin)
                if pos_fin == -1:
                    # no se encontro el fin
                    self.call_conex(-2, "Final no econtrado en paquete actual")  # es posible eliminar este mensaje
                    if pos_fin > self.max_size:
                        self.call_conex(-2, "Final no encontrado en longitud maxima - Perdida de datos")
                        # se supero el final sin encontrarlo, se elimina el inicio del paquete para posteriormente buscar otro inicio
                        self.paquete = self.paquete[pos_ini + 1:]
                        self.buscar_ini = True
                        self.buscar_fin = False
                        return ''
                    # el final puede estar en el resto del paquete, se espera el proximo paquete
                else:
                    # paquete completo
                    if pos_fin > self.max_size:
                        self.call_conex(-2, "Final encontrado pasada longitud maxima - Perdida de datos")
                        # se elimina el inicio del paquete para posteriormente buscar otro inicio
                        self.paquete = self.paquete[pos_ini + 1:]
                        self.buscar_ini = True
                        self.buscar_fin = False
                        return ''
                    else:
                        # enviar paquete
                        paq_completo = self.paquete[1:pos_fin]
                        self.buscar_ini = True
                        self.buscar_fin = False
                        # revisasr si queda paquete pendiente
                        if (len(paq_completo) + 2) == len(self.paquete):  # 2 por Inicio y Fin
                            self.paquete = ''  # no hay mas nada
                        else:
                            # enviar el paquete y rellamarse a si mismo
                            self.paquete = self.paquete[pos_fin + 1:]
                        # Envio del paquete
                        return paq_completo  # se retorna el paquete correcto

    # Log por defecto
    def __log_default(self, Texto, Modulo):
        print(Texto)

###########################################################
### METODOS ESTATICOS                                   ###
###########################################################
###########################################################
### INCREMENTAR Y OBTENER EL ID                         ###
###########################################################
def get_id(id):
    """ id es valor numerico"""
    id += 1
    if id > 99:
        id = 0
    return id
