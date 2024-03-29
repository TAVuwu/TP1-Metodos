import math
import numpy as np
from scipy.interpolate import interp1d
from scipy.interpolate import lagrange
from scipy.interpolate import CubicSpline
import matplotlib.pyplot as plt

LISTAXDISPLAY=np.linspace(-4, 4, 3000) 
LISTAXDISPLAYZOOM=np.linspace(-2,2,3000)
COLORLAGRANGE="orange"
COLORCUBIC='#ff00ff'
COLORLINEAR="#30ce2c"
COLORNEAREST='#0000ff'

def derivada_en_un_punto(x):
    return (((math.log(3) * pow(3, abs(x)) * x * math.sin(4*x) + 4 * pow(3, abs(x)) * math.cos(4*x) * abs(x) - math.log(10) * pow(3, abs(x)) * x * math.sin(4*x)) / (abs(x) * pow(10, abs(x)))) - (2 / pow(math.cosh(2*x), 2)))

def busqueda_de_raices_biseccion_real(funcion, a, b, epsilon, iteraciones_maximas):            #programado como propuesto en faires
    i = 1
    if funcion(a) * funcion(b) > 0:
        print ("Wrong a,b range")
    else:
        while (i <= iteraciones_maximas):
            r = (a + b) / 2
            if (funcion(r) == 0 or (b - a) / 2 < epsilon):
                return r
            i += 1
            if (funcion(r) * funcion(a) < 0):
                b = r
            else:
                a = r

def funcion_original(x):
    return pow(0.3, abs(x)) * math.sin(4 * x) - math.tanh(2 * x) + 2

def error_absoluto(intervalo, interp):
    error = []
    for x in intervalo:
        error.append(abs(funcion_original(x) - interp(x)))
    return error


def main():
    x_Extremos = []
    x_Extremos.append(-4)
    x_Extremos.append(busqueda_de_raices_biseccion_real(derivada_en_un_punto, -4, -3.25, 10**(-6), 1000))
    x_Extremos.append(busqueda_de_raices_biseccion_real(derivada_en_un_punto, -3.25, -2.25, 10**(-6), 1000))
    x_Extremos.append(busqueda_de_raices_biseccion_real(derivada_en_un_punto, -2.25, -1.25, 10**(-6), 1000))
    x_Extremos.append(busqueda_de_raices_biseccion_real(derivada_en_un_punto, -1.25, -0.75, 10**(-6), 1000))
    x_Extremos.append(busqueda_de_raices_biseccion_real(derivada_en_un_punto, -0.75, -0.1, 10**(-6), 1000))
    x_Extremos.append(busqueda_de_raices_biseccion_real(derivada_en_un_punto, 0.1, 0.75, 10**(-6), 1000))
    x_Extremos.append(busqueda_de_raices_biseccion_real(derivada_en_un_punto, 0.75, 1.25, 10**(-6), 1000))
    x_Extremos.append(busqueda_de_raices_biseccion_real(derivada_en_un_punto, 1.25, 2.25, 10**(-6), 1000))
    x_Extremos.append(busqueda_de_raices_biseccion_real(derivada_en_un_punto, 2.25, 3.25, 10**(-6), 1000))
    x_Extremos.append(busqueda_de_raices_biseccion_real(derivada_en_un_punto, 3.25, 4, 10**(-6), 1000))
    x_Extremos.append(4)

    y_Extremos = [funcion_original(x) for x in x_Extremos]
    
    lagrangeRegular=lagrange( np.linspace(-4,4,12),[funcion_original(i) for i in np.linspace(-4,4,12)] )
    lagrangeStrat = lagrange(x_Extremos, y_Extremos)

    sCubicRegular= CubicSpline( np.linspace(-4,4,12),[funcion_original(i) for i in np.linspace(-4,4,12)] )
    sCubicStrat = CubicSpline(x_Extremos, y_Extremos)

    sLinearRegular=interp1d( np.linspace(-4,4,12),[funcion_original(i) for i in np.linspace(-4,4,12)], "linear")
    sLinearStrat = interp1d(x_Extremos, y_Extremos,kind="linear")

    sNearestRegular=interp1d( np.linspace(-4,4,12),[funcion_original(i) for i in np.linspace(-4,4,12)], "nearest" )
    sNearestStrat = interp1d(x_Extremos, y_Extremos, kind='nearest')

    fig, ax1 = plt.subplots()
    ax1.set_title("Gráfica de la función original y aproximaciones que utilizan 12 nodos que son extremos")
    ax1.plot(LISTAXDISPLAY,[funcion_original(i) for i in LISTAXDISPLAY],c="#eff8fc",lw=24)
    ax1.plot(LISTAXDISPLAY, lagrangeStrat(LISTAXDISPLAY), label='Polinomio de Lagrange',c=COLORLAGRANGE)
    ax1.plot(LISTAXDISPLAY,[funcion_original(i) for i in LISTAXDISPLAY], label='Función original',c="black",lw=2)
    ax1.plot(LISTAXDISPLAY, sLinearStrat(LISTAXDISPLAY), label='Splines lineales',c=COLORLINEAR)
    ax1.plot(LISTAXDISPLAY, sCubicStrat(LISTAXDISPLAY), label='Splines cúbicos',c=COLORCUBIC,linestyle="dashed")
    ax1.plot(LISTAXDISPLAY, sNearestStrat(LISTAXDISPLAY), label='Splines constantes',c=COLORNEAREST,linestyle="dotted")
    ax1.set_ylim(-5,9)
    ax1.set_xlim(-4,4)
    ax1.set_xlabel('x')
    ax1.set_ylabel('y')
    ax1.legend()

    fig,ax11=plt.subplots()
    ax11.set_title("Gráfica de la función original y aproximaciones que utilizan 12 nodos que son extremos ZOOM")
    ax11.plot(LISTAXDISPLAYZOOM,[funcion_original(i) for i in LISTAXDISPLAYZOOM],c="#eff8fc",lw=24)
    ax11.plot(LISTAXDISPLAYZOOM, lagrangeStrat(LISTAXDISPLAYZOOM), label='Polinomio de Lagrange',c=COLORLAGRANGE)
    ax11.plot(LISTAXDISPLAYZOOM,[funcion_original(i) for i in LISTAXDISPLAYZOOM], label='Función original',c="black",lw=2)
    ax11.plot(LISTAXDISPLAYZOOM, sLinearStrat(LISTAXDISPLAYZOOM), label='Splines lineales',c=COLORLINEAR)
    ax11.plot(LISTAXDISPLAYZOOM, sCubicStrat(LISTAXDISPLAYZOOM), label='Splines cúbicos',c=COLORCUBIC,linestyle="dashed")
    ax11.plot(LISTAXDISPLAYZOOM, sNearestStrat(LISTAXDISPLAYZOOM), label='Splines constantes',c=COLORNEAREST,linestyle="dotted")
    ax11.set_ylim(0,4)
    ax11.set_xlim(-2,2)
    ax11.set_xlabel('x')
    ax11.set_ylabel('y')
    ax11.legend()


    fig, ax2 = plt.subplots()
    ax2.set_title("Gráfica de la función original y aproximaciones que utilizan 12 nodos equiespaciados")
    ax2.plot(LISTAXDISPLAY,[funcion_original(i) for i in LISTAXDISPLAY],c="#eff8fc",lw=24)
    ax2.plot(LISTAXDISPLAY, [funcion_original(i) for i in LISTAXDISPLAY], label='Función original',c="black",lw=2)
    ax2.plot(LISTAXDISPLAY, lagrangeRegular(LISTAXDISPLAY), label='Polinomio de Lagrange',c=COLORLAGRANGE)
    ax2.plot(LISTAXDISPLAY, sLinearRegular(LISTAXDISPLAY), label='Splines lineales',c=COLORLINEAR)
    ax2.plot(LISTAXDISPLAY, sCubicRegular(LISTAXDISPLAY), label='Splines cúbicos',linestyle="dashed",c=COLORCUBIC)
    ax2.plot(LISTAXDISPLAY, sNearestRegular(LISTAXDISPLAY), label='Splines constantes',linestyle="dotted",c=COLORNEAREST)
    ax2.set_ylim(-5,9)
    ax2.set_xlim(-4,4)
    ax2.set_xlabel('x')
    ax2.set_ylabel('y')
    ax2.legend()

    fig, ax21 = plt.subplots()
    ax2.set_title("Gráfica de la función original y aproximaciones que utilizan 12 nodos equiespaciados ZOOM")
    ax21.plot(LISTAXDISPLAYZOOM,[funcion_original(i) for i in LISTAXDISPLAYZOOM],c="#eff8fc",lw=24)
    ax21.plot(LISTAXDISPLAYZOOM, lagrangeRegular(LISTAXDISPLAYZOOM), label='Polinomio de Lagrange',c=COLORLAGRANGE)
    ax21.plot(LISTAXDISPLAYZOOM, [funcion_original(i) for i in LISTAXDISPLAYZOOM], label='Función original',c="black",lw=2)
    ax21.plot(LISTAXDISPLAYZOOM, sLinearRegular(LISTAXDISPLAYZOOM), label='Splines lineales',c=COLORLINEAR)
    ax21.plot(LISTAXDISPLAYZOOM, sCubicRegular(LISTAXDISPLAYZOOM), label='Splines cúbicos',linestyle="dashed",c=COLORCUBIC)
    ax21.plot(LISTAXDISPLAYZOOM, sNearestRegular(LISTAXDISPLAYZOOM), label='Splines constantes',linestyle="dotted",c=COLORNEAREST)
    ax21.set_ylim(0,4)
    ax21.set_xlim(-2,2)
    ax21.set_xlabel('x')
    ax21.set_ylabel('y')
    ax21.legend()

    fig, ax3 = plt.subplots()
    ax3.set_title("Errores de la función original y aproximaciones que utilizan 12 nodos equiespaciados")
    ax3.plot(LISTAXDISPLAY, error_absoluto(LISTAXDISPLAY, lagrangeRegular), label='Error Polinomio de Lagrange',c=COLORLAGRANGE)
    ax3.plot(LISTAXDISPLAY, error_absoluto(LISTAXDISPLAY, sCubicRegular), label='Error splines cúbicos',c=COLORCUBIC)
    ax3.plot(LISTAXDISPLAY, error_absoluto(LISTAXDISPLAY, sNearestRegular), label='Error splines constantes',c=COLORNEAREST)
    ax3.plot(LISTAXDISPLAY, error_absoluto(LISTAXDISPLAY, sLinearRegular), label='Error splines lineales',c=COLORLINEAR)
    ax3.set_ylim(0,15)
    ax3.set_xlabel('x')
    ax3.set_ylabel('error absoluto')
    ax3.legend()
    

    fig, ax4 = plt.subplots()
    ax4.set_title("Errores de la función original y aproximaciones que utilizan 12 nodos que son extremos")
    ax4.plot(LISTAXDISPLAY, error_absoluto(LISTAXDISPLAY, lagrangeStrat), label='Error Polinomio de Lagrange',c=COLORLAGRANGE)
    ax4.plot(LISTAXDISPLAY, error_absoluto(LISTAXDISPLAY, sCubicStrat), label='Error splines cúbicos',c=COLORCUBIC)
    ax4.plot(LISTAXDISPLAY, error_absoluto(LISTAXDISPLAY, sNearestStrat), label='Error splines constantes',c=COLORNEAREST)
    ax4.plot(LISTAXDISPLAY, error_absoluto(LISTAXDISPLAY, sLinearStrat), label='Error splines lineales',c=COLORLINEAR)
    ax4.set_ylim(0,15)
    ax4.set_xlabel('x')
    ax4.set_ylabel('error absoluto')
    ax4.legend()

    fig5, ax5 = plt.subplots()
    ax5.set_title("Errores de la función original y aproximaciones que utilizan 12 nodos equiespaciados ZOOM")
    ax5.plot(LISTAXDISPLAYZOOM, error_absoluto(LISTAXDISPLAYZOOM, lagrangeRegular), label='Error Polinomio de Lagrange',c=COLORLAGRANGE)
    ax5.plot(LISTAXDISPLAYZOOM, error_absoluto(LISTAXDISPLAYZOOM, sCubicRegular), label='Error splines cúbicos',c=COLORCUBIC)
    ax5.plot(LISTAXDISPLAYZOOM, error_absoluto(LISTAXDISPLAYZOOM, sLinearRegular), label='Error splines lineales',c=COLORLINEAR)
    ax5.plot(LISTAXDISPLAYZOOM, error_absoluto(LISTAXDISPLAYZOOM, sNearestRegular), label='Error splines constantes',c=COLORNEAREST)
    ax5.set_ylim(0,0.9)
    ax5.set_xlim(-2,2)
    ax5.set_xlabel('x')
    ax5.set_ylabel('error absoluto')
    ax5.legend()

    fig, ax6 = plt.subplots()
    ax6.set_title("Errores de la función original y aproximaciones que utilizan 12 nodos que son extremos ZOOM")
    ax6.plot(LISTAXDISPLAYZOOM, error_absoluto(LISTAXDISPLAYZOOM, lagrangeStrat), label='Error Polinomio de Lagrange',c=COLORLAGRANGE)
    ax6.plot(LISTAXDISPLAYZOOM, error_absoluto(LISTAXDISPLAYZOOM, sCubicStrat), label='Error splines cúbicos',c=COLORCUBIC)
    ax6.plot(LISTAXDISPLAYZOOM, error_absoluto(LISTAXDISPLAYZOOM, sLinearStrat), label='Error splines lineales',c=COLORLINEAR)
    ax6.plot(LISTAXDISPLAYZOOM, error_absoluto(LISTAXDISPLAYZOOM, sNearestStrat), label='Error splines constantes',c=COLORNEAREST)
    ax6.set_ylim(0,0.9)
    ax6.set_xlim(-2,2)
    ax6.set_xlabel('x')
    ax6.set_ylabel('error absoluto')
    ax6.legend(loc="upper right")

    plt.show()

if __name__ == "__main__":
    main()