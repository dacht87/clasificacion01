import sys
import json
import numpy as np
from tensorflow.keras.models import model_from_json

# Compilado en la versión 3.6.9 (default, Jan 26 2021, 15:33:00)
print("Version de Python: ", sys.version)

# Cargar la estructura del modelo desde el archivo JSON
with open('notas.json', 'r', encoding='utf-8') as json_file:
    modelo_json = json_file.read()

# Reconstruir el modelo a partir de la configuración JSON
modelo = model_from_json(modelo_json)

# Compilar el modelo (necesario si vas a usar el modelo para predicción)
modelo.compile(optimizer='adam', loss='mse')  # Ajusta el optimizador y la función de pérdida según tu modelo original


# Función para predecir el precio del departamento
def predecir_carrera(MATEMATICAS, LENGUAJE, CIENCIASNATURALES, FISICA, CIENCIASSOCIALES):
    # Crear un array con los valores de entrada
    entrada = np.array([[MATEMATICAS, LENGUAJE, CIENCIASNATURALES, FISICA, CIENCIASSOCIALES]])
    # Hacer la predicción
    carrera = modelo.predict(entrada)
    return carrera[0][0]

# Solicitar datos al usuario
MATE = int(input("Introduce la nota de matematica: "))
LEN = int(input("Introduce la nota de lenguaje: "))
CIENNAT = int(input("Introduce la nota de ciencias naturales: "))
FIS = int(input("Introduce la nota de fisica: "))
CIENSOC = int(input("Introduce la nota de ciencias sociales: "))


# Hacer la predicción
carrera_estimada = predecir_carrera(MATE,LEN,CIENNAT,FIS,CIENSOC)

if carrera_estimada>=0.5:
  print("Estudiaria Ingenieria")
else:
  print("Estudiaria Economia")
