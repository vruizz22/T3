import pandas as pd
from gurobipy import GRB
import gurobipy as gp
import locale


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

    def implementar_modelo(self):

        # Implementamos el modelo
        model = gp.Model()

        '''
        Los pesos w_i y b respectivos, donde cada
        w_i es el peso de la muestra i y b es el peso
        de la ultima columna
        '''

        # Variables de decisión
        w_i = model.addVars(self.I, lb=-GRB.INFINITY, name='w_i')
        b = model.addVar(vtype=GRB.CONTINUOUS, name='b')

        # Actualizamos el modelo
        model.update()

        # Función objetivo
        model.setObjective(sum((b + sum(w_i[i] * self.X_ir[(i, r)] for i in self.I)
                                - self.Y_r[r]) ** 2 for r in self.R), GRB.MINIMIZE)

        # Optimizamos el modelo
        model.optimize()

        # Imprimir en consola todos
        # los valores de cada variable de decisión
        for i, caracteristica in zip(self.I, leer_header('muestras.csv')):
            print(
                f'La caracteristica {caracteristica} esta asociada al peso: {round(w_i[i].x, 2)}')

        # Imprimir el valor de la cosntante b en gramos
        print(f'El valor de b es: {round(b.x, 2)} gramos')
        return model.objVal


if __name__ == '__main__':
    modelo = Modelo()
    ov = modelo.implementar_modelo()
    locale.setlocale(locale.LC_ALL, '')
    print(
        f'\033[1;32m\nEl valor entregado más cercano a Y (modelo final de la regresión) es {locale.currency(ov, grouping=True, symbol=False)} gramos.\033[0m')
