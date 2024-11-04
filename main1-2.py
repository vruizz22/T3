from gurobipy import *
import pandas as pd

# Definimos funciones: 
def definir_funcion_objetivo(model, data, lambda_val):
    funcion_objetivo = 0
    for r in range(data.shape[0]):
        term = b
        for i in range(15):
            term += w[i] * data.iloc[r, i]
        term -= data.iloc[r, 15]
        funcion_objetivo += term * term
    
    l1_penalty = lambda_val * sum(z[i] for i in range(15))
    funcion_objetivo += l1_penalty
    
    return funcion_objetivo

def resolver_modelo(model):
    model.optimize()
    print("________________________________________________")
    print("Resultados Problema 3.2 Formulación Matematica 1\n")
    print(f'Valor de la función objetivo: {model.ObjVal:.4f}\n')
    print(f'Valor Lamda: {lambda_val} (valor aproximado)\n')
    print("Detalles de los pesos de la transformación:\n")
    for i in range(15):
        parametro = data.columns[i] 
        print(f'W{i+1} = {w[i].X} correspondiente al peso del dato {parametro} ')
    print(f'b = {b.X} (gr)')
    
    print("\nEs importante tener en cuenta que el renderizado del modelo puede generar una carga considerable en el procesador, la cual varía según el tipo de computadora desde la cual se ejecute. Esto se debe a la utilización de hilos o threads. En un computador menos potente, w3 tiene un peso significativo, mientras que en un computador más potente, w7 son más influyentes. Lo anteriormente mencionado tiene una relación directa con la parte 3 del presente modelo.")

# Importar los datos del archivo CSV:
data = pd.read_csv('muestras.csv')

# Crear variables y modelo:
model = Model('Resultados Problema 3.2 Formulación Matematica 1')

w = {}
z = {}

for i in range(15):
    w[i] = model.addVar(lb=-GRB.INFINITY, ub=GRB.INFINITY, name=f'w{i}')
    z[i] = model.addVar(lb=0, ub=GRB.INFINITY, name=f'z{i}')

b = model.addVar(lb=-GRB.INFINITY, ub=GRB.INFINITY, name="b")

model.update()

# Añadir restricciones:
for i in range(15):
    model.addConstr(-z[i] <= w[i])
    model.addConstr(z[i] >= w[i])

lambda_val = 1300
"""lambda_val = 1400"""

# Definir la función objetivo:
funcion_objetivo = definir_funcion_objetivo(model, data, lambda_val)
model.setObjective(funcion_objetivo, GRB.MINIMIZE)

# Resolver el modelo:
resolver_modelo(model)

#Parametros optimos:
print("________________________________________________")
print("Parámetros asociados a los pesos significativos:\n")
for i in range(15):
    if abs(w[i].X) > 10**-11:
        parametro = data.columns[i] 
        print(f'Parámetro W{i+1} correspondiente al peso del dato {parametro}')
        
#Generar archivo csv pesos significantes:
indices_pesos_significativos = [i for i in range(15) if abs(w[i].X) > 10**-11]
data_pesos_significativos = data.copy()

# Eliminar las columnas que no son significativas:
columnas_no_significativas = [i for i in range(15) if i not in indices_pesos_significativos]
data_pesos_significativos.drop(data_pesos_significativos.columns[columnas_no_significativas], axis=1, inplace=True)

# Guardar el DataFrame en un archivo CSV:
data_pesos_significativos.to_csv('datos_pesos_significativos.csv', index=False)

print("\nSe guardaron los datos de pesos significativos en el archivo CSV 'datos_pesos_significativos.csv' para su posterior uso.")