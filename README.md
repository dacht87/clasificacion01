Pasos para ejecutar el Jetson nano:

1. Clonar el repositorio:
jetson@jetson-desktop:~/clasificacion01$ git clone https://github.com/dacht87/clasificacion01/
jetson@jetson-desktop:~/clasificacion01$ ls
 clasifica.py   notas_old.json     notas.weights_old.h5   requirements.txt
 notas.json     notas.weights.h5   programa.py           'Tabla 2.xlsx'

Los archivos _old funcionan para Arquitectura X86.

2. Ejecutar el contenedor utilizando la imagen: nvcr.io/nvidia/l4t-tensorflow:r32.6.1-tf2.5-py3
Soporte Python3 y Tensorflow 2.5 
https://catalog.ngc.nvidia.com/orgs/nvidia/containers/l4t-tensorflow

jetson@jetson-desktop:~$ sudo docker run -it --rm --runtime nvidia -v /home/jetson/clasificacion01/:/app nvcr.io/nvidia/l4t-tensorflow:r32.6.1-tf2.5-py3 bash

root@ba242de9d60a:/#

3. Listar los archivos del proyecto en el contenedor:
root@ba242de9d60a:/# ls /app
'Tabla 2.xlsx'   notas.json         notas.weights_old.h5   programa.py
 clasifica.py    notas.weights.h5   notas_old.json         requirements.txt

 4. Ejecutar la aplicación programa.py:
root@ba242de9d60a:/app# python3 programa.py
