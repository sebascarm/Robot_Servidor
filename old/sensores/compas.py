import smbus
import math
import subprocess


class Compas (object):
    def __init__(self):
        self.bus = smbus.SMBus(1)   #bus GPIO
        self.compas_address = 0x1e

        self.x_offset = 66
        self.y_offset = -214
        self.write_byte(0, 0b01110000)  # Set to 8 samples @ 15Hz
        self.write_byte(1, 0b00100000)  # 1.3 gain LSb / Gauss 1090 (default)
        self.write_byte(2, 0b00000000)  # Continuous sampling
        self.scale = 0.92

    def read_byte(self, adr):
        return self.bus.read_byte_data(self.compas_address, adr)

    def read_word(self, adr):
        high = self.bus.read_byte_data(self.compas_address, adr)
        low = self.bus.read_byte_data(self.compas_address, adr + 1)
        val = (high << 8) + low
        return val

    def read_word_2c(self, adr):
        val = self.read_word(adr)
        if val >= 0x8000:
            return -((65535 - val) + 1)
        else:
            return val

    def write_byte(self, adr, value):
        self.bus.write_byte_data(self.compas_address, adr, value)

    def angulo(self):
        #NorteCasa = 318
        NorteCasa = 316

        x_out = (self.read_word_2c(3) - self.x_offset) * self.scale
        y_out = (self.read_word_2c(7) - self.y_offset) * self.scale
        z_out = (self.read_word_2c(5)) * self.scale
        bearing = math.atan2(y_out, x_out)
        if bearing < 0:
            bearing += 2 * math.pi
        # Ajuste seba para acomodar al angulo de la casa
        if math.degrees(bearing) > NorteCasa:
            angulo = math.degrees(bearing) - NorteCasa
        else:
            angulo = math.degrees(bearing) + (360 - NorteCasa)
        # Ajuste de angulo adicional x seba
        if angulo < 93:  # 90 grados reales
            angulo_final = angulo / 93 * 90
        elif angulo < 176:  # 180 grados reales
            angulo_final = ((angulo - 93) / (176 - 93) * (180 - 90)) + 90
        elif angulo < 270:  # 270 grados reales
            angulo_final = ((angulo - 176) / (270 - 176) * (270 - 180)) + 180
        # elif angulo < 360:  # 360 grados reales
        #    angulo_final = angulo / 360 * 360
        else:
            angulo_final = angulo
        return angulo_final
