from gurobipy import *
import pandas as pd

#Definir funciones:
def definir_funcion_objetivo(model, data):
    funcion_objetivo = 0
    for r in range(100):
        term = b
        for i in range(5):
            term += w[i] * data.iloc[r, i]
        term -= data.iloc[r, 5]
        funcion_objetivo += term * term
    return funcion_objetivo

def resolver_modelo(model):
    model.optimize()
    print("________________________________________________\n")
    print("Resultados Problema 3.3 Formulación Matematica 1\n")
    print("Modelo final de regresión:\n")
    
    print("Estructura:")
    print("Y = b + w1*x1 + w2*x2 + w3*x3 + w4*x4 + w5*x5")
    
    print("\nFunción:")
    modelo_final_regresion = f"Y = {b.X}"
    for i in range(5):
        modelo_final_regresion += f" + {w[i].X} * x{[i+1]}"
    print(modelo_final_regresion)
    print("\nLa función Y corresponde a la cantidad de gramos de relleno  para una almohadas de alta gama de un cliente dada las siguientes carracteristicas:\n")
    for i in range(5):
          print(f"x{[i+1]} = {data.columns[i]}")
          
    print("\nAdemás, se presenta los siguientes pesos:\n")

    for i in range(5):
        print(f'W{i+1} = {w[i].X}')
    print(f'b = {b.X} cota inferior de gramos de relleno para almohadas')

# Importar los datos del archivo CSV:
data = pd.read_csv('datos_pesos_significativos.csv')

# Crear variables y modelo
model = Model('Resultados Problema 3.3 Formulación Matematica 1')

w = {}
for i in range(5):
    w[i] = model.addVar(lb=-GRB.INFINITY, ub=GRB.INFINITY, name=f'w{i}')
b = model.addVar(lb=-GRB.INFINITY, ub=GRB.INFINITY, name="b")

model.update()

# Definir la función objetivo
funcion_objetivo = definir_funcion_objetivo(model, data)
model.setObjective(funcion_objetivo, GRB.MINIMIZE)

# Resolver el modelo
resolver_modelo(model)

