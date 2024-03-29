import matplotlib.pyplot as plt
import math
import numpy as np
from scipy.interpolate import CubicSpline
from scipy.interpolate import interp1d
from scipy.interpolate import lagrange
import csv

def error_en_t(lista_x, lista_y, x_interpoladas, y_interpoladas):
    error = []
    for t in range(100):
        error.append(math.sqrt(pow(lista_x[t] - x_interpoladas[t], 2) + pow(lista_y[t] - y_interpoladas[t], 2)))        #distancia entre vector posicion ground truth y vector posicion interpolado
    return error

def main():

    lista_x_gt = []
    lista_y_gt = []

    lista_x_sensado = []
    lista_y_sensado = []

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
            lista_x_sensado.append(float(x))
            lista_y_sensado.append(float(y))

    tiempo_ground_truth = np.linspace(0, 99, 100)
    tiempo_sensado = np.linspace(0, 99, 10)

    xSplinesC = CubicSpline(tiempo_sensado, lista_x_sensado)
    ySplinesC = CubicSpline(tiempo_sensado, lista_y_sensado)
    x_interpoladas_con_cubic_spline=[xSplinesC(t) for t in tiempo_ground_truth]
    y_interpoladas_con_cubic_spline=[ySplinesC(t) for t in tiempo_ground_truth]

    xSplinesL = interp1d(tiempo_sensado, lista_x_sensado)
    ySplinesL = interp1d(tiempo_sensado, lista_y_sensado)
    x_interpoladas_con_linear_spline=[xSplinesL(t) for t in tiempo_ground_truth]
    y_interpoladas_con_linear_spline=[ySplinesL(t) for t in tiempo_ground_truth]

    xLagrange = lagrange(tiempo_sensado, lista_x_sensado)
    yLagrange = lagrange(tiempo_sensado, lista_y_sensado)
    x_interpoladas_con_lagrange=[xLagrange(t) for t in tiempo_ground_truth]
    y_interpoladas_con_lagrange=[yLagrange(t) for t in tiempo_ground_truth]

    error_absoluto_cubicos = error_en_t(lista_x_gt, lista_y_gt, x_interpoladas_con_cubic_spline, y_interpoladas_con_cubic_spline)
    error_absoluto_lineales = error_en_t(lista_x_gt, lista_y_gt,x_interpoladas_con_linear_spline, y_interpoladas_con_linear_spline)
    error_absoluto_lagrange = error_en_t(lista_x_gt, lista_y_gt, x_interpoladas_con_lagrange, y_interpoladas_con_lagrange)

    fig, ax1 = plt.subplots()
    ax1.set_title("Trayectoria original e interpolaciones")
    ax1.plot(lista_x_gt, lista_y_gt,color = '#0000ff' , label='Trayectoria original')
    ax1.plot(x_interpoladas_con_linear_spline, y_interpoladas_con_linear_spline, color = '#ff00ff',label='Splines lineales')
    ax1.plot(x_interpoladas_con_cubic_spline, y_interpoladas_con_cubic_spline,color = '#00ff00', label='Splines cúbicos')
    ax1.plot(x_interpoladas_con_lagrange, y_interpoladas_con_lagrange, color = 'orange',label='polinomios de Lagrange')
    ax1.set_xlabel('x')
    ax1.set_ylabel('y')
    ax1.legend()

    fig, ax2 = plt.subplots()
    ax2.set_ylim(0,9)
    ax2.set_title("Error absoluto de splines cúbicos a lo largo de t")
    ax2.plot(tiempo_ground_truth, error_absoluto_cubicos)
    ax2.axhline(y=0, linestyle='--', color='r')
    ax2.set_xlabel('t')
    ax2.set_ylabel('error absoluto')
    ax2.legend()

    fig, ax3 = plt.subplots()
    ax3.set_ylim(0,9)
    ax3.set_title("Error absoluto de splines lineales a lo largo de t")
    ax3.plot(tiempo_ground_truth, error_absoluto_lineales)
    ax3.axhline(y=0, linestyle='--', color='r')
    ax3.set_xlabel('t')
    ax3.set_ylabel('error absoluto')
    ax3.legend()

    fig, ax4 = plt.subplots()
    ax4.set_ylim(0,9)
    ax4.set_title("Error absoluto de Lagrange a lo largo de t")
    ax4.plot(tiempo_ground_truth, error_absoluto_lagrange)
    ax4.axhline(y=0, linestyle='--', color='r')
    ax4.set_xlabel('t')
    ax4.set_ylabel('error absoluto')
    ax4.legend()

    plt.show()

if __name__ == "__main__":
    main()