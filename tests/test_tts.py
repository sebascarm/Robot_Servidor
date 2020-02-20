from gtts import gTTS
#from playsound import playsound
import pygame
#pygame.mixer.init()
pygame.mixer.init(24500)

NOMBRE_ARCHIVO = "sonido_generado.mp3"
print("Iniciando")
tts = gTTS('Iniciando Robot.', lang='es-us')
tts.save(NOMBRE_ARCHIVO)
print("save")
pygame.mixer.music.load(NOMBRE_ARCHIVO)
print("load")
pygame.mixer.music.play()
print("payed")
while pygame.mixer.music.get_busy() == True:
    continue
print("free")


print("NUEVO")
tts = gTTS('Iniciando sistemas de Inteligencia Artificial.', lang='es-us')
tts.save(NOMBRE_ARCHIVO)
print("save")
pygame.mixer.music.load(NOMBRE_ARCHIVO)
print("load")
pygame.mixer.music.play()
print("payed")
while pygame.mixer.music.get_busy() == True:
    continue
print("free")

print("NUEVO")
tts = gTTS('Cargando elementos de arranque.', lang='es-us')
tts.save(NOMBRE_ARCHIVO)
print("save")
pygame.mixer.music.load(NOMBRE_ARCHIVO)
print("load")
pygame.mixer.music.play()
print("payed")
while pygame.mixer.music.get_busy() == True:
    continue
print("free")

print("NUEVO")
tts = gTTS('Inicializando sistemas de reconocimiento.', lang='es-us')
tts.save(NOMBRE_ARCHIVO)
print("save")
pygame.mixer.music.load(NOMBRE_ARCHIVO)
print("load")
pygame.mixer.music.play()
print("payed")
while pygame.mixer.music.get_busy() == True:
    continue
print("free")

print("NUEVO")
tts = gTTS('Proceso basico de inicialización finalizado.', lang='es-us')
tts.save(NOMBRE_ARCHIVO)
print("save")
pygame.mixer.music.load(NOMBRE_ARCHIVO)
print("load")
pygame.mixer.music.play()
print("payed")
while pygame.mixer.music.get_busy() == True:
    continue
print("free")
