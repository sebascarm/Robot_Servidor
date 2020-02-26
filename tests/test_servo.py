""" Prueba de uso de binarios """
import time
# Esto es para poder hacer el from desde un nivel atras y funciona con launch.json
import os, sys

BASE_PATH = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(BASE_PATH)

from sensores.servo import Servo
import time

servo1 = Servo()
servo2 = Servo()
servo_rizq = Servo()
servo_rder = Servo()


servo1.config(1,90,-90, 85, False)
servo2.config(2,25,0,95, True)

servo_rizq.config_continuo(3,351,401,301)
servo_rder.config_continuo(0,353,403,303, True)

def loop():
    print("mover servo")

    for x in range(0, 100):
        for x in range(0, 90):
            print(x)
            servo2.angulo(x-50)
            servo1.angulo(-45 + x)
            time.sleep(0.02)

        for x in range(90, 0,-1):
            print(x)
            servo2.angulo(x -50)
            servo1.angulo(-45 + x)
            time.sleep(0.02)

def loop2():
    servo1.angulo(0)
    time.sleep(1)
    servo1.angulo(-20)
    time.sleep(1)
    servo1.angulo(-40)
    time.sleep(1)
    servo1.angulo(-20)
    time.sleep(1)
    servo1.angulo(0)

def ruedas():
    servo_rizq.mover(1)
    servo_rder.mover(1)
    time.sleep(1)
    servo_rizq.mover(2)
    servo_rder.mover(2)
    time.sleep(1)
    servo_rizq.mover(3)
    servo_rder.mover(3)
    time.sleep(1)
    servo_rizq.mover(0)
    servo_rder.mover(0)

# loop()
loop2()
#ruedas()

print("fin")