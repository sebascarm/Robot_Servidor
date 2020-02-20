Robot Server Version 0.8.8
=====================
* 20/02/2020
    * clase webcam       v1.7 (reintento de conexion)   
    * clase thread_admin v2.3 (diccionario)
    * clase Servidor_TCP v3.7 (log de th en callback)
    * main2 (inicial)    v1.1
    * clase image_send   v1.0
    * clase comunicacion v3.7 (log)
* Previo
    * clase comunicacion
    * timer v1.1 (fsp y delay)
    * Correccion webcam

Versiones:
* Python 3.6.9 (Linux PC)
* Requerido:
    * gTTS
    * pyGame
    * Opencv

-----------
## Carpetas
-----------


* Componentes
    * Clases y objetos de uso comun
* Tmp
    * archivos temporales
* Actividad
* Comunicacion
* ia

--------------
## GIT + Github
--------------
Sofware Git: https://git-scm.com

 - Se instala con las herramientas de unix adicionales

### Ubicacion
- D:\QNapDrive\Programacion\Web\Git

### Comandos
- Abrir carpeta con Gitbash
- `git init` (iniciamos git en la carpeta)
- `git status` (ver los archivos)
- `git add` (agrega archivo (usar tambien luego de cambios en un archivo)
- `git add .` (agrega todos los archivos)
- `git commit` (commit)
- `git commit -m "descrip"` (commit)
- `git log` (ver el estado de los commit)
- `git restore` (restaurar un archivo dado antes del commit)
- `git diff` (ver las diferencias de un archivo)
- crear archivo .gitignore (el contenido sera ignorado)
- `git branch` (muestra las ramas del programa (master por defecto)
- `git branch nomb` (crea una rama nomb)
- `git checkout nomb` (entra en la rama nomb)

### Usuario
- git config --global user.email "sebascarm@gmail.com"
- git config --global user.name "sebascar"

### GitHub
- Crear proyecto
- git remote add origin
- git push -u origin master
- git pull // trae los cambios del servidor
- git clone DIRECCION // se trae a local los archivos del repositorio

### Actualizar el -gitignore
- git rm -r --cached .
- git add .
- git commit -m "Atualizando .gitignore para..."

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
### Metodo 2 (Instalado en Raspberry)
http://blog.enriqueoriol.com/2014/06/virtualenvwrapper-tu-virtualenv.html
```
workon entorno-cv   # Activar el enotorno virtual
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
----------------
Instalar PYGAME
===============
```
sudo pip3 install pygame

```

----------------
Instalar otros
===============
```
sudo apt-get install libatlas-base-dev
sudo pip3 install numpy scipy
sudo pip3 install numpy

sudo apt-get install libhdf5-dev
sudo apt-get install libhdf5-serial-dev

```
PIPCONFIG

```
per-user: $HOME/.config/pip/pip.conf
global: /etc/pip.conf

# Agregar repositiorio
[global]
extra-index-url=https://www.piwheels.org/simple
```
