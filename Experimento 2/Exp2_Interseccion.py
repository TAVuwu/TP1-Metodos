import numpy as np
from scipy import interpolate
from scipy import optimize
from scipy.misc import derivative
from matplotlib import pyplot as plt
import csv

def metodo_newton(f, x0, tol, max_iter):            #programado como propuesto en faires
    i=1
    while i<=max_iter:
        x1=x0-f(x0)/derivative(f,x0)
        if abs(x1-x0)<tol:
            return x1
        x0=x1
        i+=1
    return "fracaso"


def main():

    lista_x_gt = []
    lista_y_gt = []

    lista_x1_sensado = []
    lista_y1_sensado = []

    lista_x2_sensado = []
    lista_y2_sensado = []

    with open('mnyo_ground_truth.csv', 'r') as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=' ')
        for row in csv_reader:
            x, y = row
            lista_x_gt.append(float(x))
            lista_y_gt.append(float(y))

    with open('mnyo_mediciones.csv', 'r') as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=' ')
        for row in csv_reader:
            x, y = row
            lista_x1_sensado.append(float(x))
            lista_y1_sensado.append(float(y))

    with open('mnyo_mediciones2.csv', 'r') as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=' ')
        for row in csv_reader:
            x, y = row
            lista_x2_sensado.append(float(x))
            lista_y2_sensado.append(float(y))

    momentos_ground_truth = np.linspace(0, 99, 100)
    momentos_sensados_1 = np.linspace(0, 99, 10)

    #interpolar x1(t) e y1(t) por separado
    splines_x_1 = interpolate.CubicSpline(momentos_sensados_1, lista_x1_sensado)
    splines_y_1 = interpolate.CubicSpline(momentos_sensados_1, lista_y1_sensado)

    splines_2=interpolate.CubicSpline(lista_x2_sensado, lista_y2_sensado)

    fig, ambastrayectorias = plt.subplots()
    ambastrayectorias.set_title('Ambas trayectorias visualizadas')
    ambastrayectorias.plot(lista_x_gt, lista_y_gt, color = '#ff00ff' , label='Vehiculo 1 según mediciones ground truth')
    ambastrayectorias.scatter(lista_x1_sensado, lista_y1_sensado,color = '#ff00ff',label='Vehiculo 1, nodos sensados')
    ambastrayectorias.plot(splines_x_1(momentos_ground_truth), splines_y_1(momentos_ground_truth), color = '#00ff00',label='Vehiculo 1 con splines cúbicos')
    ambastrayectorias.scatter(lista_x2_sensado, lista_y2_sensado, color = '#0000ff',label='Vehiculo 2, nodos sensados')
    ambastrayectorias.set_xlabel('x')
    ambastrayectorias.set_ylabel('y')
    ambastrayectorias.set_ylim(0,6)
    ambastrayectorias.set_xlim(0,35)
    ambastrayectorias.plot(np.linspace(5,25,500), splines_2(np.linspace(5,25,500)),color = '#0000ff',label='Vehiculo 2 con splines cúbicos')

    #evaluemos a los splines de la seguna trayectoria en x1(t), e igualemos a y1(t)
    composicion_T1parametrizada_con_T2funcion= lambda t: splines_2(splines_x_1(t))-splines_y_1(t)
    t_sol=metodo_newton(composicion_T1parametrizada_con_T2funcion,30,0.0001,1000)
    ambastrayectorias.scatter(splines_x_1(t_sol),splines_y_1(t_sol),color='black',label='Intersección obtenida usando método de Newton',zorder=10)
    ambastrayectorias.legend()
    print(splines_x_1(t_sol), splines_y_1(t_sol))
    plt.show()

if __name__ == "__main__":
    main()