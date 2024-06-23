import pandas as pd
from gurobipy import GRB
import gurobipy as gp
import locale


def leer_archivo(archivo: str) -> list:
    # dejar todos los valores como float
    return pd.read_csv(archivo).values.astype(float)


class Modelo:

    def __init__(self) -> None:

        # Lectura de archivo una sola vez
        datos = leer_archivo('muestras.csv')

        # Características más importantes:
        # ['peso(kg)', 'estatura(cm)', 'contorno_cuello(cm)',
        # 'contorno_caja_toraxica(cm)', 'largo_del_brazo(cm)']

        self.E = [1, 2, 7, 11, 13]
        self.R = range(1, datos.shape[0] + 1)

        # Lectura de archivos y creación de parametros
        # X_ir tiene la muestra i para la persona r
        # Hasta la penultima columna son los valores de X_ir
        self.X_ir = {
            (i, r): datos[r - 1, i - 1]
            for i in self.E for r in self.R
        }

        # La última columna de muestras.csv es el valor de Y_r
        self.Y_r = {
            r: datos[r - 1, -1]
            for r in self.R
        }

        # X_i es el conjunto de las características más importantes
        # donde X_i \in E
        self.X_i = {
            i: str(datos[:, i - 1].tolist())
            for i in self.E
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
        w_i = model.addVars(self.E, vtype=GRB.CONTINUOUS, name='w_i')
        b = model.addVar(vtype=GRB.CONTINUOUS, name='b')

        # Actualizamos el modelo
        model.update()

        # Función objetivo
        model.setObjective(sum((b + sum(w_i[i] * self.X_ir[(i, r)] for i in self.E)
                                - self.Y_r[r]) ** 2 for r in self.R), GRB.MINIMIZE)

        # Optimizamos el modelo
        model.optimize()

        # Imprimir en consola todos
        # los valores de cada variable de decisión
        caracteristicas = ['peso(kg)', 'estatura(cm)', 'contorno_cuello(cm)',
                           'contorno_caja_toraxica(cm)', 'largo_del_brazo(cm)']
        for i, caracteristica in zip(self.E, caracteristicas):
            print(
                f'La caracteristica {caracteristica} esta asociada al peso: {round(w_i[i].x, 2)}')

        # Imprimir el valor de la cosntante b en gramos
        print(f'El valor de b es: {round(b.x, 2)} gramos')

        # FInalmente imprimir un string que represente
        # el modelo final de la regresión que se le entregara a la empresa
        for i in self.E:
            print(
                f'\nY_{i}={round(w_i[i].x, 2)} * {self.X_i[i]} + {round(b.x, 2)}, donde Y_{i} es el valor de la muestra {i} en gramos\nx_{i} es el valor de la característica {i} en la muestra\n')
        print('donde x_1 es el peso(kg), x_2 es la estatura(cm), x_7 es el contorno_cuello(cm), x_11 es el contorno_caja_toraxica(cm) y x_13 es el largo_del_brazo(cm)')
        print(f'\nFinalmente Y = Y_1 + Y_2 + Y_7 + Y_11 + Y_13 gramos')
        return model.objVal


if __name__ == '__main__':
    modelo = Modelo()
    ov = modelo.implementar_modelo()
    locale.setlocale(locale.LC_ALL, '')
    print(
        f'\033[1;32m\nEl valor entregado más cercano a Y es {locale.currency(ov, grouping=True, symbol=False)} gramos.\033[0m')
