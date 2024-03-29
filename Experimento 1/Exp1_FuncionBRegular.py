import math
import numpy as np
from scipy.interpolate import lagrange
from scipy.interpolate import CubicSpline
from scipy.interpolate import interp1d
import matplotlib.pyplot as plt

def funcionb(x, y):
    z = 0.75 * pow(math.e, -(pow((10*x-2),2)/4)-pow((9*y-2),2)/4) + 0.65 * pow(math.e, -(pow((9*x+1),2)/9)-pow((10*y+1),2)/2) + 0.55 * pow(math.e, -(pow((9*x-6),2)/4)-pow((9*y-3),2)/4) - 0.01 * pow(math.e, -(pow((9*x-7),2)/4)-pow((9*y-3),2)/4)
    return z

def fijar_x_para_f(x,f):
    return lambda y: f(x,y)

def fijar_y_para_f(y,f):
    return lambda x: f(x,y)

def error_absoluto_entre_dos_funciones_en(interp,funcion,p):
    return abs(interp(p)-funcion(p))

def error_abs_maximo_entre_dos_funciones(interp,funcion):
    max=0
    for p in np.linspace(-1, 1, 400):
        if max<error_absoluto_entre_dos_funciones_en(interp,funcion,p): max=error_absoluto_entre_dos_funciones_en(interp,funcion,p)
    return max

def main():
    intervalo=np.linspace(-1,1,50)
    figs,graficoErrores = plt.subplots(2,2,figsize=(15,15))
    figs,graficoInterp = plt.subplots(2,2,figsize=(15,15),subplot_kw={'projection': '3d'})
    graficoErrores[0,0].set_title('Error máximo de interpolación con polinomios de Lagrange, con nodos en grilla nxn')
    graficoErrores[0,1].set_title('Error máximo de interpolación con splines constantes, con nodos en grilla nxn')
    graficoErrores[1,0].set_title('Error máximo de interpolación con splines lineales, con nodos en grilla nxn')
    graficoErrores[1,1].set_title('Error máximo de interpolación con splines cúbicos, con nodos en grilla nxn')
    for a in range(2):
        for b in range(2):
            graficoErrores[a,b].set_xlabel('n')
            graficoErrores[a,b].set_ylabel('error absoluto máximo')
            graficoErrores[a,b].grid()
    graficoInterp[0,0].set_title('Función original (en rojo) y (aproximación con polinomios de Lagrange)+2')
    graficoInterp[0,1].set_title('Función original (en rojo) y (aproximación con splines constantes)+1')
    graficoInterp[1,0].set_title('Función original (en rojo) y (aproximación con splines lineales)+1')
    graficoInterp[1,1].set_title('Función original (en rojo) y (aproximación con splines cúbicos)+1')

    for tamaño_grilla in range(3, 41):
        nodos_a_utilizar = np.linspace(-1, 1, tamaño_grilla)
        erroresMaximosLagrange = []
        erroresMaximosSCubicos = []
        erroresMaximosSLineales = []
        erroresMaximosSConstantes = []
        for x in intervalo:      #fijar un valor de x
            f_xFija = fijar_x_para_f(x,funcionb)
            splinescubicosf_xFija = CubicSpline(nodos_a_utilizar,[f_xFija(y) for y in nodos_a_utilizar])
            splineslinealesf_xFija=interp1d(nodos_a_utilizar,[f_xFija(y) for y in nodos_a_utilizar],"linear")
            splinesconstantesf_xFija=interp1d(nodos_a_utilizar,[f_xFija(y) for y in nodos_a_utilizar],"nearest")
            poliLagrange_f_xFija=lagrange(nodos_a_utilizar,[f_xFija(y) for y in nodos_a_utilizar])

            #### Errores
            erroresMaximosLagrange.append(error_abs_maximo_entre_dos_funciones(poliLagrange_f_xFija,f_xFija))
            erroresMaximosSCubicos.append(error_abs_maximo_entre_dos_funciones(splinescubicosf_xFija,f_xFija))
            erroresMaximosSLineales.append(error_abs_maximo_entre_dos_funciones(splineslinealesf_xFija,f_xFija))
            erroresMaximosSConstantes.append(error_abs_maximo_entre_dos_funciones(splinesconstantesf_xFija,f_xFija))

            # #### Plotear interpolaciones cuando grilla 10x10
            if tamaño_grilla==8:
                z_xFija = []
                zInterpolados_Xfija_Scubicos = []
                zInterpolados_Xfija_SLineales = []
                zInterpolados_Xfija_SConstantes = []
                zInterpolados_Xfija_Lagrange = []
                for y in intervalo:
                    z_xFija.append(f_xFija(y))
                    zInterpolados_Xfija_Scubicos.append(splinescubicosf_xFija(y)+1)
                    zInterpolados_Xfija_SLineales.append(splineslinealesf_xFija(y)+1)
                    zInterpolados_Xfija_SConstantes.append(splinesconstantesf_xFija(y)+1)
                    zInterpolados_Xfija_Lagrange.append(poliLagrange_f_xFija(y)+2)
                for a in range(2):
                    for b in range(2):
                        graficoInterp[a,b].plot3D([x]*50,intervalo,z_xFija,color='red')
                graficoInterp[0,0].plot3D([x]*50,intervalo,zInterpolados_Xfija_Lagrange,color='green')
                graficoInterp[0,1].plot3D([x]*50,intervalo,zInterpolados_Xfija_SConstantes,color='blue')
                graficoInterp[1,0].plot3D([x]*50,intervalo,zInterpolados_Xfija_SLineales,color='orange')
                graficoInterp[1,1].plot3D([x]*50,intervalo,zInterpolados_Xfija_Scubicos,color='purple')

        for y in intervalo:      #fijar un valor de y
            f_yFija = fijar_y_para_f(y,funcionb)    #definir una funcion que dependa solo de x
            splinescubicosf_yFija=CubicSpline(nodos_a_utilizar,[f_yFija(x) for x in nodos_a_utilizar])
            splineslinealesf_yFija=interp1d(nodos_a_utilizar,[f_yFija(x) for x in nodos_a_utilizar],"linear")
            splinesconstantesf_yFija=interp1d(nodos_a_utilizar,[f_yFija(x) for x in nodos_a_utilizar],"nearest")
            poliLagrange_f_yFija=lagrange(nodos_a_utilizar,[f_yFija(x) for x in nodos_a_utilizar])

            #### Errores
            erroresMaximosLagrange.append(error_abs_maximo_entre_dos_funciones(poliLagrange_f_yFija,f_yFija))
            erroresMaximosSCubicos.append(error_abs_maximo_entre_dos_funciones(splinescubicosf_yFija,f_yFija))
            erroresMaximosSLineales.append(error_abs_maximo_entre_dos_funciones(splineslinealesf_yFija,f_yFija))
            erroresMaximosSConstantes.append(error_abs_maximo_entre_dos_funciones(splinesconstantesf_yFija,f_yFija))

            #### Plotear interpolaciones cuando grilla 10x10
            if tamaño_grilla==10:
                z_yFija = []
                zInterpolados_Yfija_Scubicos = []
                zInterpolados_Yfija_SLineales = []
                zInterpolados_Yfija_SConstantes = []
                zInterpolados_Yfija_Lagrange = []
                for x in intervalo:
                    z_yFija.append(f_xFija(x))
                    zInterpolados_Yfija_Scubicos.append(splinescubicosf_yFija(x)+1)
                    zInterpolados_Yfija_SLineales.append(splineslinealesf_yFija(x)+1)
                    zInterpolados_Yfija_SConstantes.append(splinesconstantesf_yFija(x)+1)
                    zInterpolados_Yfija_Lagrange.append(poliLagrange_f_yFija(x)+2)
                for a in range(2):
                    for b in range(2):
                        graficoInterp[a,b].plot3D(intervalo,[y]*50,z_yFija,color='red')
                graficoInterp[0,0].plot3D(intervalo,[y]*50,zInterpolados_Yfija_Lagrange,color='green')
                graficoInterp[0,1].plot3D(intervalo,[y]*50,zInterpolados_Yfija_SConstantes,color='blue')
                graficoInterp[1,0].plot3D(intervalo,[y]*50,zInterpolados_Yfija_SLineales,color='orange')
                graficoInterp[1,1].plot3D(intervalo,[y]*50,zInterpolados_Yfija_Scubicos,color='purple')

        graficoErrores[0,0].scatter(tamaño_grilla, max(erroresMaximosLagrange), color='green')
        graficoErrores[0,1].scatter(tamaño_grilla, max(erroresMaximosSConstantes), color='blue')
        graficoErrores[1,0].scatter(tamaño_grilla, max(erroresMaximosSLineales), color='orange')
        graficoErrores[1,1].scatter(tamaño_grilla, max(erroresMaximosSCubicos), color='purple')


        graficoErrores[0,0].set_ylim(0,3250)
        graficoErrores[0,1].set_ylim(0,0.7)
        graficoErrores[1,0].set_ylim(0,0.7)
        graficoErrores[1,1].set_ylim(0,0.7)

    plt.show()

if __name__ == "__main__":
    main()