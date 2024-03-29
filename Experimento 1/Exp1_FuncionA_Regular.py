import numpy as np
from scipy.interpolate import lagrange
from scipy.interpolate import CubicSpline
from scipy.interpolate import interp1d
from scipy.interpolate import approximate_taylor_polynomial
import matplotlib.pyplot as plt
from mpl_toolkits.axes_grid1.inset_locator import inset_axes

def funcion_original(x):
    return pow(0.3, np.abs(x)) * np.sin(4 * x) - np.tanh(2 * x) + 2

def splines_cubicos_de_fa_con_n_nodos_equiespaciados(n):
    return CubicSpline(np.linspace(-4,4,n),[funcion_original(x) for x in np.linspace(-4,4,n)])

def splines_lineales_de_fa_con_n_nodos_equiespaciados(n):
    return interp1d(np.linspace(-4,4,n),[funcion_original(x) for x in np.linspace(-4,4,n)],"linear")

def splines_constantes_de_fa_con_n_nodos_equiespaciados(n):
    return interp1d(np.linspace(-4,4,n),[funcion_original(x) for x in np.linspace(-4,4,n)],"nearest")

def lagrange_de_fa_con_n_nodos_equiespaciados(n):
    return lagrange(np.linspace(-4, 4, n),[funcion_original(x) for x in np.linspace(-4,4,n)])

def calcular_error_dada_interp_y_punto(interp,x):
    return abs(interp(x)-funcion_original(x))

def calc_error_promedio_dada_interp(interp):    #evalua en 1000 puntos equiespaciados
    sum=0
    for x in np.linspace(-4, 4, 1000):
        sum+=calcular_error_dada_interp_y_punto(interp,x)
    return sum/1000

def calc_error_maximo_dada_interp(interp):      #evalua en 1000 puntos equiespaciados
    max=0
    for x in np.linspace(-4, 4, 1000):
        if max<calcular_error_dada_interp_y_punto(interp,x): max=calcular_error_dada_interp_y_punto(interp,x)
    return max

def main():
    lista_x = np.linspace(-4, 4, 1000)
    lista_y=[]
    for i in lista_x:
        lista_y.append(funcion_original(i))

    figs, funciones = plt.subplots(2,2,figsize=(15,15))
    figs, errores = plt.subplots(2,2,figsize=(15,15))
    figs, taylor = plt.subplots(1,2,figsize=(15,15))

    for a in range(2):
        for b in range(2):
            funciones[a,b].set_ylim(0,4)
            errores[a,b].set_ylim(0,1.5)
            errores[a,b].set_xlabel('cantidad nodos')
            errores[a,b].set_ylabel('error absoluto máximo')
            errores[a,b].set_xticks([2]+[x for x in range(10,110,10)])
            errores[a,b].grid()
    errores[0,0].set_ylim(0,1200)
    errores[0,0].set_xticks([2]+[x for x in range(10,60,10)])
    errores00inset_zoomin = inset_axes(errores[0,0], width="40%", height="40%", loc='upper right')
    errores00inset_zoomin.set_xlim(2, 15)
    errores00inset_zoomin.set_ylim(0, 4)
    errores00inset_zoomin.set_xticks([x for x in range(2,16,2)])
    errores00inset_zoomin.grid()
    errores00inset_zoomout = inset_axes(errores[0,0], width="40%", height="40%", loc='lower right')
    errores00inset_zoomout.xaxis.tick_top()
    errores00inset_zoomout.set_xlim(30, 40)
    errores00inset_zoomout.set_ylim(4000, 600000)
    errores00inset_zoomout.set_xticks([x for x in range(30,40)])
    errores00inset_zoomout.grid()
    taylor[1].set_ylim(0,120)

    ######## mostrar lagrange polinomios contra funcion original

    funciones[0,0].set_title('Gráfica de funcion original + polinomios de lagrange')
    for n in range(2,16):
        poli=lagrange_de_fa_con_n_nodos_equiespaciados(n)
        if n%5==0: funciones[0,0].plot(lista_x,[poli(x) for x in lista_x],label=f"Nodos = {n}")
    funciones[0,0].plot(lista_x, lista_y, label='Función original')
    funciones[0,0].legend(loc='upper right', fontsize='small')
    
########################  grafico error maximo lagrange a medida que se añaden nodos
    
    #errores[0,0].set_title('Gráfica de error maximo de lagrange, creciente a medida que se agregan nodos')
    lista_errores_max=[]
    lista_n= []
    for n in range(2,100):
        lista_n.append(n)
        poli=lagrange_de_fa_con_n_nodos_equiespaciados(n)
        lista_errores_max.append(calc_error_maximo_dada_interp(poli))
    errores[0,0].scatter(lista_n,lista_errores_max,s=10,c="blue")
    errores[0,0].plot(lista_n,lista_errores_max)
    errores00inset_zoomin.scatter(lista_n,lista_errores_max,c="blue")
    errores00inset_zoomin.plot(lista_n,lista_errores_max)
    errores00inset_zoomout.scatter(lista_n,lista_errores_max,c="blue")
    errores00inset_zoomout.plot(lista_n,lista_errores_max)

################### mostrar cubic splines contra funcion original

    funciones[0,1].set_title('Gráfica de funcion original + aproximaciones con splines cubicos')
    for n in range(2,16):
        splines=splines_cubicos_de_fa_con_n_nodos_equiespaciados(n)
        if n%5==0: funciones[0,1].plot(lista_x, [splines(x) for x in lista_x], label=f"Nodos = {n}")
    funciones[0,1].plot(lista_x,lista_y, label="Funcion original")
    funciones[0,1].legend(loc='upper right', fontsize='small')
    
############# mostrar error maximo de splines a medida que se añaden nodos

    #errores[0,1].set_title('Gráfica de error maximo de splines cubicos, decreciente a medida que se agregan nodos')
    lista_errores_max=[]
    lista_n=[]
    for n in range(2,100):
        lista_n.append(n)
        splines=splines_cubicos_de_fa_con_n_nodos_equiespaciados(n)
        lista_errores_max.append((calc_error_maximo_dada_interp(splines)))
    errores[0,1].plot(lista_n,lista_errores_max)
    errores[0,1].scatter(lista_n,lista_errores_max,s=10,c="blue")


###########  mostrar splines lineales contra funcion original
    
    funciones[1,0].set_title('Gráfica de funcion original + aproximaciones con splines lineales')
    for n in range(2,16):
        splines=splines_lineales_de_fa_con_n_nodos_equiespaciados(n)
        if n%5==0: funciones[1,0].plot(lista_x, [splines(x) for x in lista_x], label=f"Nodos = {n}")
    funciones[1,0].plot(lista_x,lista_y, label="Funcion original")
    funciones[1,0].legend(loc='upper right', fontsize='small')

############# mostrar error maximo de splines a medida que se añaden nodos

    #errores[1,0].set_title('Gráfica de error maximo de splines lineales, decreciente a medida que se agregan nodos')
    lista_errores_max=[]
    lista_n=[]
    for n in range(2,100):
        lista_n.append(n)
        splines=splines_lineales_de_fa_con_n_nodos_equiespaciados(n)
        lista_errores_max.append((calc_error_maximo_dada_interp(splines)))
    errores[1,0].plot(lista_n,lista_errores_max)
    errores[1,0].scatter(lista_n,lista_errores_max,s=10,c="blue")

##########  mostrar aproximacion tipo "nearest" (splines constantes) contra la funcion original
    
    funciones[1,1].set_title('Gráfica de funcion original + aproximaciones con splines constantes')
    for n in range(2,16):
        splines=splines_constantes_de_fa_con_n_nodos_equiespaciados(n)
        if n%5==0:funciones[1,1].plot(lista_x, [splines(x) for x in lista_x], label=f"Nodos = {n}")
    funciones[1,1].plot(lista_x,lista_y, label="Funcion original")
    funciones[1,1].legend(loc='upper right', fontsize='small')

    
############# mostrar error maximo de nearest a medida que se toman en cuenta mas derivadas
    
    #errores[1,1].set_title('Gráfica de error maximo de splines constantes, decreciente a medida que se aumentan nodos')
    lista_errores_max=[]
    lista_n=[]
    for n in range(2,100):
        lista_n.append(n)
        splines=splines_constantes_de_fa_con_n_nodos_equiespaciados(n)
        lista_errores_max.append((calc_error_maximo_dada_interp(splines)))
    errores[1,1].plot(lista_n,lista_errores_max)
    errores[1,1].scatter(lista_n,lista_errores_max,s=10,c="blue")

######Extra
###########  mostrar polinomios de taylor contra funcion original
    
    taylor[0].set_title('Gráfica de funcion original + aproximaciones con taylors')
    for n in range(2,6):
        poli=approximate_taylor_polynomial(funcion_original, 0, n,0)
        taylor[0].plot(lista_x, [poli(x) for x in lista_x], label=f"Taylor grado = {n}")
    taylor[0].plot(lista_x,lista_y, label="Funcion original")
    taylor[0].set_ylim(0,4)
    taylor[0].set_xlim(-4,4)
    taylor[0].legend(loc='upper right', fontsize='small')

############# mostrar error maximo de taylor a medida que se toman en cuenta mas derivadas
    
    taylor[1].set_title('Gráfica de error maximo de taylor, creciente a medida que se aumenta el grado')
    lista_errores_max=[]
    lista_n=[]
    for n in range(2,10):
        lista_n.append(n)
        poli=approximate_taylor_polynomial(funcion_original, 0, n,0)
        lista_errores_max.append((calc_error_maximo_dada_interp(poli)))
    taylor[1].scatter(lista_n,lista_errores_max)
    
############# 
    
    plt.show()


if __name__=="__main__":
    main()