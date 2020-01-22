Python & Robot
=====================

Versiones
---------

* Python 3.6.9 (Linux PC)
```
beautifulsoup4        4.8.2         #gTTS     
certifi               2019.11.28    #gTTS     
chardet               3.0.4         #gTTS     
Click                 7.0           #gTTS     
gTTS                  2.1.0         #gTTS     
gTTS-token            1.1.3         #gTTS     
idna                  2.8           #gTTS     
imutils               0.5.3         #OpenCV (utilidades graficas)
numpy                 1.18.1        #OpenCV
opencv-contrib-python 4.1.2.30      #OpenCV
pip                   9.0.1     
pkg-resources         0.0.0     
pygame                1.9.6         #pyGame
requests              2.22.0        #gTTS         
setuptools            39.0.1    
six                   1.13.0        #gTTS
soupsieve             1.9.5         #gTTS
urllib3               1.25.7        #gTTS
```



Entrar en la terminal
=====================
ssh pi@192.168.0.26

### Ejecutar en terminal en folder del ejecutable (test1 = nombre de archivo posiblemente)
```
$ cd Robot/Debug/Servidor.. 
python3 -m ptvsd --host 192.168.0.26 --port 3000 --wait -m main
```

### En el codigo:

```
import ptvsd
ptvsd.enable_attach(address=('192.168.0.26', 3000), redirect_output=True)
# Pause
ptvsd.wait_for_attach()
```

#### Copiar de otro ejemplo el archivo .vscode
#### rasp

---------------
Python
===============
## Version instalada 3.8.1 (32 bits)

## Entorno Virtual

## Instalar entorno virtual (solo linux - metodo facil)
```
sudo ap-get install python3-venv
```
## Crear entorno virtual en directorio
```
python3 -m venv carpeta-env  # Crea la carpeta carpeta-env)
cd carpeta-env
```
#### Activar en Windows
```
Scripts\activate.bat        # Activamos el entorno
Scripts\deactivate.bat      # Desctiva el entorno
```
#### Activar en Linux
```
source carpeta-env/bin/activate
deactivate                  # comando solo sin ruta
```
## Comandos PIP

## Instalar entorno virtual (solo linux - metodo facil)
```
pip list --format=columns   # vemos los elementos instalados

```
---------------
Instalar gTTS
===============
https://pypi.org/project/gTTS/1.1.8/

### Texto a vos mediante Google (utilizado por robot)

```
pip install gTTS
```
---------------
Instalar OpenCV
===============
https://www.pyimagesearch.com/opencv-tutorials-resources-guides/
## Metodo rapido con Pip
Se puede realizar en un entorno virtual
```
pip install opencv-contrib-python
```
### Testing
```
pip install imutils

```

