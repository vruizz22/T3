import pandas as pd
from gurobipy import GRB
import gurobipy as gp

datos = pd.read_csv("muestras.csv")
titulos = datos.columns

#Conjuntos

R = range(len(datos))
I = range(len(datos.iloc[0])-1)

#Parametros del modelo

x_ir = {}

y_r = {}

for i in I:
    for r in R:
        x_ir[(i,r)] = datos.iloc[r,i]

for r in R:
    y_r[r] = datos.iloc[r,-1]

#Modelo

model = gp.Model()

#Variables

w_i = model.addVars(I , vtype = GRB.CONTINUOUS, name = "w_i")

b = model.addVar(vtype = GRB.CONTINUOUS, name = "b")

z_i = model.addVars(I , vtype = GRB.CONTINUOUS, name = "z_i")

lambda_0 = 10**-11

model.update()

#Restricciones

for i in I:
    model.addConstr(-z_i[i] <= w_i[i], name = "r1")
    model.addConstr(w_i[i] <= z_i[i], name = "r2")

# Funcion objetivo

while True:
    model.setObjective(sum((b + sum(w_i[i]*x_ir[(i,r)] for i in I) - y_r[r] )**2 for r in R) + lambda_0 * sum(z_i[i] for i in I), GRB.MINIMIZE)
    model.optimize()
    
    c = 0
    for i in I:
        if abs(w_i[i].x) >= 10**-11:
            c += 1
    if c == 5:
        break
    lambda_0 *= 10

E = []    

for i in I:
    if abs(w_i[i].x) >= 10**-11:
        E.append(i)


print("El conjunto de caracteristicas mas importantes E es:", E)
print("El valor de lambda utilziado fue:", lambda_0)





