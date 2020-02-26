""" Prueba de uso de binarios """
# Esto es para poder hacer el from desde un nivel atras y funciona con launch.json
import os, sys
BASE_PATH = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(BASE_PATH)

from ia.tts import TTS

hablar = TTS()
hablar.config()

hablar.say("hola")
hablar.say("hola, como estas hoy?")
