import pandas as pd
from gurobipy import GRB
import gurobipy as gp


def leer_archivo(archivo: str) -> list:
    # dejar todos los valores como float
    return pd.read_csv(archivo).values.astype(float)


def leer_header(archivo: str) -> list:
    return pd.read_csv(archivo).columns


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

    def implementar_modelo(self, lambda_val):

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
        # z_i varible que representa el valor absoluto de w_i
        z_i = model.addVars(self.I, vtype=GRB.CONTINUOUS, name='z_i')

        # Actualizamos el modelo
        model.update()

        # Restricciones
        model.addConstrs(
            (-z_i[i] <= w_i[i] for i in self.I),
            name='restriccion_absoluta'
        )
        model.addConstrs(
            (w_i[i] <= z_i[i] for i in self.I),
            name='restriccion_absoluta_2'
        )

        # Función objetivo
        model.setObjective(
            sum((b + sum(w_i[i] * self.X_ir[(i, r)] for i in self.I) - self.Y_r[r]) ** 2 for r in self.R) +
            lambda_val * sum(z_i[i] for i in self.I), GRB.MINIMIZE
        )

        # Optimizamos el modelo
        model.optimize()

        # asociar las caracteristicas a los
        # pesos w_i
        caracteristicas = {
            i: (caracteristicas, w_i[i].x) for i, caracteristicas in zip(self.I, leer_header('muestras.csv'))
        }
        return caracteristicas

    def encontrar_caracteristicas_significativas(self):
        lambda_val = 1e-5  # Valor inicial de lambda
        while True:
            caracteristicas = self.implementar_modelo(lambda_val)
            # Contar pesos significativamente distintos de cero
            pesos_no_nulos = sum(1 for i in self.I if abs(
                caracteristicas[i][1]) > 1e-11)
            if pesos_no_nulos == 5:
                break
            lambda_val *= 10  # Incrementar lambda

        # Imprimir características significativas y valor de lambda
        caracteristicas_significativas = [
            caracteristicas[i][0] for i in self.I if abs(caracteristicas[i][1]) > 1e-11]
        print(
            f'Características más importantes: {caracteristicas_significativas}')
        print(f'Valor de lambda utilizado: {lambda_val}')


if __name__ == '__main__':
    modelo = Modelo()
    modelo.encontrar_caracteristicas_significativas()
