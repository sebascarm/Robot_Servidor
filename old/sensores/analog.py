#!/usr/bin/env python
import time
import math

from smbus import SMBus

bus = SMBus(1)

adjustment_value = 0.97

def read_ain(i):    
    global bus
    bus.write_byte(0x48, i)
    bus.read_byte(0x48)#first 2 are last state, and last state repeated.
    bus.read_byte(0x48)
    return bus.read_byte(0x48)

# Function to convert data to voltage level,
# rounded to specified number of decimal places.
def ConvertVolts(data,places):
  #volts = (data * 3.3) / float(1023)
  volts = (data * 3.3) / float(255)
  volts = round(volts,places)
  return volts

# Function to calculate temperature from
# TMP36 data, rounded to specified
# number of decimal places.
def ConvertTemp(data,places):
 
  # ADC Value
  # (approx)  Temp  Volts
  #    0      -50    0.00
  #   78      -25    0.25
  #  155        0    0.50
  #  233       25    0.75
  #  310       50    1.00
  #  465      100    1.50
  #  775      200    2.50
  # 1023      280    3.30
 
  temp = ((data * 330)/float(1023))-50
  temp = round(temp,places)
  return temp

while(True):
    temp = read_ain(0)
    luz  = read_ain(10)
    print ('temp:' + str(temp))
    print ('luz:' + str(luz))
    print ('pote:' + str(read_ain(2)))	
    print ('anal:' + str(read_ain(3)))
     
    analogVal = temp
    Vr = 3.3 * float(analogVal) / 255
    Rt = 10000 * Vr / (5 - Vr)
    temp2 = 1/(((math.log(Rt / 10000)) / 3950) + (1 / (273.15+25)))
    temp2 = temp2 - 273.15
    print ('temp: ', temp2, 'C')
    print ("---")
    
    # Read the light sensor data
    #light_level = ReadChannel(light_channel)
    light_volts = ConvertVolts(luz,2)
 
    # Read the temperature sensor data
    #temp_level = ReadChannel(temp_channel)
    temp_volts = ConvertVolts(temp,2)
    tempC       = ConvertTemp(temp,2)

    # Print out results
    print ("--------------------------------------------")
    print ("Light: {} ({}V)".format(luz , light_volts))
    print ("Temp : {} ({}V) {} deg C".format(temp,temp_volts,tempC))

    tmp = temp*(255-125)/255+125 # LED won't light up below 125, so convert '0-255' to '125-255'
    print ("TMP: {}".format(tmp))

    time.sleep(0.5)#sec