import random
import time
from mpl_toolkits.mplot3d import axes3d
import matplotlib.pyplot as plt
import numpy as np
from matplotlib import cm
from matplotlib.ticker import LinearLocator, FormatStrFormatter
import math
from enum import Enum

class FunctionType(Enum):
    ROSENBROCK = 1
    GRIEWANK = 2
    RASTRIGIN = 3

def calc_function(x,y, function_type):
    if function_type == FunctionType.ROSENBROCK:
        return ((1 - x) ** 2) + (100 * ((y - x ** 2) ** 2))
    elif function_type == FunctionType.GRIEWANK:
        return (x**2)/4000 + (y**2)/4000 - (math.cos(x)*math.cos(y/math.sqrt(2))) + 1
    elif function_type == FunctionType.RASTRIGIN:
        return 20 + (x**2 - 10*math.cos(2*math.pi*x)) + (y**2 - 10*math.cos(2*math.pi*y))

def calc_function_np(x, y, function_type):
    if function_type == FunctionType.ROSENBROCK:
        return ((1 - x) ** 2) + (100 * ((y - x ** 2) ** 2))
    elif function_type == FunctionType.GRIEWANK:
        return (x**2)/4000 + (y**2)/4000 - (np.cos(x)*np.cos(y/np.sqrt(2))) + 1
    elif function_type == FunctionType.RASTRIGIN:
        return 20 + (x**2 - 10*np.cos(2*np.pi*x)) + (y**2 - 10*np.cos(2*np.pi*y))

def get_max_and_min(function_type):
    if function_type == FunctionType.ROSENBROCK:
        return (-3, 3, -3, 3, 0.5)
    elif function_type == FunctionType.GRIEWANK:
        return (-600, 600, -600, 600, 50)
    elif function_type == FunctionType.RASTRIGIN:
        return (-5.12, 5.12, -5.12, 5.12, 0.3)


def particle_swarm(nrParticle, nrIteratii, function_type):
    (x_min, x_max, y_min, y_max, meshgrid_pas) = get_max_and_min(function_type)
    plt.ion()
    name = []
    particlesX = []
    particlesY = []
    particlesV1 = []
    particlesV2 = []
    particlesPB = []
    particlesPBX = []
    particlesPBY = []
    fi1 = 1.4
    fi2 = 1.4
    gb = -1
    gbx = -1
    gby = -1
    #initializare particule
    # si determinarea gb dupa initializare
    print("Initial particles: ")
    for i in range(0, nrParticle):
        particlesX.append(random.uniform(x_min, x_max))
        particlesY.append(random.uniform(y_min, y_max))
        particlesV1.append(0/1)
        particlesV2.append(0/1)
        particlesPB.append(calc_function(particlesX[i], particlesY[i], function_type))
        particlesPBX.append(particlesX[i])
        particlesPBY.append(particlesY[i])
        name.append(i)
        if gb < 0 or gb > particlesPB[i]:
            gb = particlesPB[i]
            gbx = particlesX[i]
            gby = particlesY[i]
    print("initial gb: "+ str(gb))
    for i in range(0, nrParticle):
        print(str(particlesX[i]) + " " + str(particlesY[i]) + " -> " + str(particlesPB[i]))
    print("\n")
    #inceputul iterarii
    fig = plt.figure()
    ax = axes3d.Axes3D(fig)
    for t in range(0, nrIteratii):
        X = np.arange(x_min, x_max, meshgrid_pas)
        Y = np.arange(y_min, y_max, meshgrid_pas)
        X, Y = np.meshgrid(X, Y)
        Z = calc_function_np(X, Y, function_type)
        ax.plot_surface(X, Y, Z, rstride=1, cstride=1, cmap='hot')
        for i in range(0, len(name)):
            plt.annotate(name[i], (particlesX[i], particlesY[i]))
        plt.xlabel('X')
        plt.ylabel('Y')
        #pentru fiecare particula recalculam pb-ul
        min = gb
        minx = gbx
        miny = gby
        for i in range(0, nrParticle):
            u1 = random.uniform(0, 1)
            u2 = random.uniform(0, 1)
            u3 = random.randint(0,1)
            if u3 == 0:
                u3 = -1
            u4 = random.randint(0,1)
            if u4 == 0:
                u4 = -1
            v1 = 0.7*particlesV1[i] + (fi1 * u1 * (particlesPBX[i] - particlesX[i])) + (fi2 * u2 * (gbx - particlesX[i]))
            v2 = 0.7*particlesV2[i] + (fi1 * u1 * (particlesPBY[i] - particlesY[i])) + (fi2 * u2 * (gby - particlesY[i]))
            x = (particlesX[i] + v1)
            y = (particlesY[i] + v2)
            aux = 1
            if x > 0:
                if x > x_max:
                    x = x_max
            else:
                if x < x_min:
                   x = x_min
            if y > 0:
                if y > y_max:
                    y = y_max
            else:
                if y < y_min:
                    y = y_min
            print(str(x))
            print(str(y))
            latest = calc_function(x,y, function_type)
            #daca noua pozitie a particulei ne da un pb mai bun, mutam particula
            particlesV1[i] = v1
            particlesV2[i] = v2
            particlesX[i] = x
            particlesY[i] = y
            if latest < particlesPB[i]:
                particlesPB[i] = latest
                particlesPBX[i] = x
                particlesPBY[i] = y
            if latest < min:
                min = latest
                minx = x
                miny = y
        #daca am gasit un gb mai bun, il inlocuim
        if min < gb:
            gb = min
            gbx = minx
            gby = miny
        ax.plot(particlesX, particlesY, particlesPB, 'bo')
        plt.show()
        print('Pas '+ str(t))
        plt.pause(0.00000001)
        ax.clear()
    X = np.arange(x_min, x_max, meshgrid_pas)
    Y = np.arange(y_min, y_max, meshgrid_pas)
    X, Y = np.meshgrid(X, Y)
    Z = calc_function_np(X, Y, function_type)
    ax.plot_surface(X, Y, Z, rstride=1, cstride=1, cmap='hot')
    ax.plot(particlesX, particlesY, particlesPB, 'ro')
    print("Finish: ")
    for i in range(0, nrParticle):
        print(str(particlesX[i]) + " " + str(particlesY[i]) + " -> " + str(particlesPB[i]))
    print("Global best: " + str(gb) + " la "+ str(gbx) + " " + str(gby))
    ax.plot(particlesX, particlesY, particlesPB, 'bo')
    plt.show()
    plt.pause(1000)
    plt.ioff()

particle_swarm(40, 100, function_type=FunctionType.ROSENBROCK)
