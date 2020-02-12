#!/usr/bin/env python
import time
import math
#board pins
#pin 3=SDA
#pin 5=SCL

from smbus import SMBus

bus = SMBus(1)
temp_pin=0
light_pin=1

adjustment_value = 0.97

def read_ain(i):    
    global bus
    bus.write_byte(0x48, i)
    bus.read_byte(0x48)#first 2 are last state, and last state repeated.
    bus.read_byte(0x48)
    return bus.read_byte(0x48)

while(True):
    temp = read_ain(0)
    print ('temp:' + str(temp))
    print ('luz:' + str(read_ain(1)))
    print ('pote:' + str(read_ain(2)))	
    print ('anal:' + str(read_ain(3)))	
    print ("---")
     
    

    B = 3977.0 # Thermistor constant from thermistor datasheet
    B = 1 # Thermistor constant from thermistor datasheet
    R0 = 10000.0 # Resistance of the thermistor being used
    t0 = 273.15 # 0 deg C in K
    t25 = t0 + 25.0 # 25 deg C in K
    # Steinhart-Hart equation
    inv_T = 1/t25 + 1/B * math.log(temp/R0)
    T = (1/inv_T - t0) * adjustment_value
    
    print ('cent:' + str(T))
    T2 = T * 9.0 / 5.0 + 32.0 # Convert C to F	
    print ('cent2:' + str(T2))

    airtemp = ((temp - 1.8308))/-0.0325	
    print ('cent3:' + str(airtemp))

    
    analogVal = temp
    Vr = 3.3 * float(analogVal) / 255
    Rt = 10000 * Vr / (5 - Vr)
    temp2 = 1/(((math.log(Rt / 10000)) / 3950) + (1 / (273.15+25)))
    temp2 = temp2 - 273.15
    print ('temperature = ', temp2, 'C')
	
    #print get_temp()
    #print get_light_level()
    time.sleep(0.5)#sec
