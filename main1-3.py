from gurobipy import *
import pandas as pd

# Definimos funciones: 
def definir_funcion_objetivo(model, data):
    funcion_objetivo = 0
    for r in range(100):
        term = b
        for i in range(15):
            term += w[i] * data.iloc[r, i]
        term -= data.iloc[r, 15]
        funcion_objetivo += term **2
    return funcion_objetivo

def resolver_modelo(model):
    model.optimize()
    print("________________________________________________")
    print("Resultados Problema 3.1 Formulación Matematica 1\n")
    print(f'Valor de la función objetivo: {model.ObjVal:.4f}\n')
    for i in range(15):
        parametro = data.columns[i] 
        print(f'W{i+1} = {w[i].X} correspondiente al peso del dato {parametro} ')
    print(f'b = {b.X} (gr)')
    
    """print("Comparación con valores reales:")
    for r in range(100):
        predicted = b.X
        for i in range(15):
            predicted += w[i].X * data.iloc[r, i]
        real = data.iloc[r, 15]
        print(f'Dato {r+1}: Predicho = {predicted:.4f}, Real = {real:.4f}')"""

# Importar los datos del archivo CSV:
data = pd.read_csv('muestras.csv')

# Crear variables y modelo:
model = Model('Resultados Problema 3.1 Formulación Matematica 1')

w = {}
for i in range(15):
    w[i] = model.addVar(lb=-GRB.INFINITY, ub=GRB.INFINITY, name=f'w{i}')
b = model.addVar(lb=-GRB.INFINITY, ub=GRB.INFINITY, name="b")

model.update()

# Definir la función objetivo:
funcion_objetivo = definir_funcion_objetivo(model, data)
model.setObjective(funcion_objetivo, GRB.MINIMIZE)

# Resolver el modelo:
resolver_modelo(model)