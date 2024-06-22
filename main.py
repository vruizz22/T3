import pandas as pd
from gurobipy import GRB
import gurobipy as gp
import locale


def leer_archivo(archivo: str) -> list:
    return pd.read_csv(archivo).values


def leer_header(archivo: str) -> list:
    return pd.read_csv(archivo).columns


print(leer_header('muestras.csv'))


class Modelo:

    def __init__(self) -> None:

        # Lectura de archivo una sola vez
        datos = leer_archivo('muestras.csv')

        # Conjunto de muestras
        # Son 16 medidas, donde tenemos xi para i = 1, 2, ..., 15
        # y la última columna es el valor de Y_r
        self.R = range(1, datos.shape[0] + 1)
        self.I = range(1, datos.shape[1])

        # Lectura de archivos y creación de parametros
        # X_ir tiene la muestra i para la persona r
        # Hasta la penultima columna son los valores de X_ir
        self.X_ir = {
            (i, r): datos[r - 1, i - 1]
            for i in self.I for r in self.R
        }

        # La última columna de muestras.csv es el valor de Y_r
        self.Y_r = {
            r: datos[r - 1, -1]
            for r in self.R
        }
        print(self.Y_r)
        print(self.X_ir)

    def implementar_modelo(self):
        # Implementamos el modelo
        model = gp.Model()

        '''
        Los pesos w_i y b respectivos, donde cada
        w_i es el peso de la muestra i y b es el peso
        de la ultima columna
        '''

        # Variables de decisión
        w_i = model.addVars(self.I, vtype=GRB.CONTINUOUS, name='w_i')
        b = model.addVar(vtype=GRB.CONTINUOUS, name='b')

        # Actualizamos el modelo
        model.update()

        # Restricciones
        '''
        model.addConstrs(
            (S_mt[m, t - 1] + a_mt[m, t] == S_mt[m, t] + quicksum(b_mit[m, i, t] for i in self.I)
             for m in self.M for t in self.T if t >= 2),
            name='restriccion_inventario'
        )
        model.addConstrs(
            (a_mt[m, 1] == S_mt[m, 1] + quicksum(b_mit[m, i, 1] for i in self.I)
             for m in self.M),
            name='restriccion_inventario_inicial'
        )
        N = 10000000000
        model.addConstrs(
            (N * z_it[i, t] >= x_mit[m, i, t]
             for m in self.M for i in self.I for t in self.T),
            name='restriccion_infraestructura'
        )
        model.addConstrs(
            (quicksum(y_it[i, t] for t in self.T) <= 1 - self.EI_i[i]
             for i in self.I),
            name='restriccion_infraestructura_unica'
        )
        model.addConstrs(
            (quicksum(x_mit[m, i, t] * self.phi_m[m]
             for m in self.M) <= self.K for i in self.I for t in self.T),
            name='restriccion_capacidad'
        )
        model.addConstrs(
            (z_it[i, t] <= quicksum(y_it[i, t_] for t_ in range(1, t + 1)) + self.EI_i[i]
             for i in self.I for t in self.T),
            name='restriccion_infraestructura_existente'
        )
        model.addConstrs(
            (z_it[i, t] >= y_it[i, t] + z_it[i, t - 1]
             for i in self.I for t in self.T if t >= 2),
            name='restriccion_infraestructura_existente_2'
        )
        model.addConstrs(
            (z_it[i, 1] >= y_it[i, 1] + self.EI_i[i]
             for i in self.I),
            name='restriccion_infraestructura_existente_3'
        )
        model.addConstrs(
            (quicksum(z_it[j, t] for j in self.I if j != i and float(self.d_ij[(i, j)]) <= float(self.AM)) >= z_it[i, t]
             for i in self.I for t in self.T),
            name='restriccion_distancia'
        )
        model.addConstrs(
            (x_mit[m, i, t] == b_mit[m, i, t] + x_mit[m, i, t - 1]
             for m in self.M for i in self.I for t in self.T if t >= 2),
            name='restriccion_cantidad_cargadores'
        )
        model.addConstrs(
            (x_mit[m, i, 1] == b_mit[m, i, 1] + self.EC_mi[m, i]
             for m in self.M for i in self.I),
            name='restriccion_cantidad_cargadores_inicial'
        )
        model.addConstrs(
            (d_mit[m, i, t] <= self.D_mit[m, i, t]
             for m in self.M for i in self.I for t in self.T),
            name='restriccion_demanda'
        )
        model.addConstrs(
            (self.delta * d_mit[m, i, t] <= x_mit[m, i, t] * self.phi_m[m]
             for m in self.M for i in self.I for t in self.T),
            name='restriccion_carga'
        )
        '''

        # Función objetivo
        print("AHORA LA FUNCION OBJETIVO")
        objetivo = gp.quicksum((b + gp.quicksum(w_i[i] * float(self.X_ir[(i, r)])
                                                for i in self.I) - float(self.Y_r[r])) ** 2 for r in self.R)
        model.setObjective(objetivo, GRB.MINIMIZE)

        # Optimizamos el modelo
        model.optimize()

        if model.status == GRB.INFEASIBLE:
            # Imprimir las restricciones que hacen que el modelo sea infactible
            print('El modelo es infactible')
            model.computeIIS()
            model.write('modelo.ilp')
            return None

        elif model.status == GRB.UNBOUNDED:
            print('El modelo es no acotado')
            return None

        elif model.status == GRB.INF_OR_UNBD:
            print('El modelo es infactible o no acotado')
            return None

        else:
            # Imprimir en consola todos
            # los valores de cada variable de decisión
            for v in model.getVars():
                print(f'{v.varName} = {v.x}')
            return model.objVal


if __name__ == '__main__':
    modelo = Modelo()
    ov = modelo.implementar_modelo()
    if ov is not None:
        locale.setlocale(locale.LC_ALL, '')
        print(
            f'\033[1;32mEl valor entregado más cercano es {locale.currency(ov, grouping=True)}\033[0m')
