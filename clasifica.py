import numpy as np
import pandas as pd
import sys
import io
import tensorflow as tf
from tensorflow.keras import Sequential,layers

# Asegúrate de que la salida estándar use UTF-8
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

print(tf.__version__)
print("Num GPUs Available: ", len(tf.config.list_physical_devices('GPU')))

path="Tabla 2.xlsx"
#dataset=pd.read_excel(path,0)
#dataset=pd.read_excel(path,sheet_name="Lince")
dataset=pd.read_excel(path, engine='openpyxl')
dataset.head(7)

dataset.info()

dataset=dataset.dropna()

def crear_cu(dato):
  if dato=="ECONOMIA":
    return 0
  elif dato=="INGENIERIA":
    return 1

dataset["CU"]=dataset["CARRERA UNIVERSITARIA"].apply(crear_cu)

dataset.head()

data_train=dataset.sample(frac=0.8,random_state=0)
data_test=dataset.drop(data_train.index)

print(data_train)
print(data_test)

columns_input=["MATEMATICAS",
               "LENGUAJE",
               "CIENCIAS NATURALES",
               "FISICA",
               "CIENCIAS SOCIALES"]
columns_output="CU"


#Datos de entrenamiento
x_train=data_train[columns_input]
y_train=data_train[columns_output]

#Datos de test
x_test=data_test[columns_input]
y_test=data_test[columns_output]

#Valores estadísticos de las entradas de entrenamiento
train_stats=x_train.describe()
train_stats=train_stats.transpose()
print(train_stats)

def escala(x):
  return (x-train_stats["min"])/(train_stats["max"]-train_stats["min"])

xe_train=escala(x_train)
xe_test=escala(x_test)

print(x_train)
print(xe_train)

#Modelo con Red Neuronal Clasificación

modelo=Sequential([   layers.Input(shape=[len(xe_train.keys())]),
                      layers.Dense(32,activation="relu"),
                      layers.Dense(1,activation="sigmoid")

])

modelo.summary()

from tensorflow import optimizers

#loss="binary_crossentropy","accuracy"

#op= optimizers.SGD(learning_rate=0.01)
#op= optimizers.RMSprop(learning_rate=0.01)
op= optimizers.Adam(learning_rate=0.1)

modelo.compile(optimizer=op,loss="binary_crossentropy",metrics=["accuracy"])

hist=modelo.fit(xe_train,y_train,epochs=500)

loss_bce=hist.history["loss"]
loss_acc=hist.history["accuracy"]
epochs=range(1,len(loss_bce)+1)

#Test
y_test_est=modelo.predict(xe_test)
y_test_real=np.array(y_test).reshape(-1,1)
print(np.round(y_test_est))
print(y_test_real)

from sklearn.metrics import accuracy_score
acc_test=accuracy_score(y_test_real,np.round(y_test_est))
print("acc_test:",acc_test)

#Predicción
x_new=pd.DataFrame({"MATEMATICAS":[10],
                    "LENGUAJE":[17],
                    "CIENCIAS NATURALES":[19],
                    "FISICA":[11],
                    "CIENCIAS SOCIALES":[18]})

xe_new=escala(x_new)
y_pred=modelo.predict(xe_new)
print(y_pred)


if y_pred[0][0]>=0.5:
  print("Estudiaría Ingenieria")
else:
  print("Estudiaría Economía")

##Guardar el modelo entrenado

#Arquitectura de la red Neuronal
path_json="notas.json"

#Pesos Finales
path_h5="notas.weights.h5"


with open(path_json,"w") as json_file:
  json_file.write(modelo.to_json())
json_file.close()

modelo.save_weights(path_h5)

print("Se guardo el modelo!!!!")
