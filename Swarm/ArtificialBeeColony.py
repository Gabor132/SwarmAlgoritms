import random
import time
from mpl_toolkits.mplot3d import axes3d
import matplotlib.pyplot as plt
import numpy as np
from matplotlib import cm
from matplotlib.ticker import LinearLocator, FormatStrFormatter
from enum import Enum
import operator
import math


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
        return (-5.12, 5.12, -5.12, 5.12, 0.5)


class FoodSourceStatus(Enum):
    OCCUPIED = 1
    DEPLETED = 2


class FoodSource:
    def __init__(self, x: float = 0, y: float = 0, function_type:FunctionType = FunctionType.ROSENBROCK):
        self.x = x
        self.y = y
        self.function_type = function_type
        self.value = calc_function(x, y, function_type=function_type)
        self.status = FoodSourceStatus.OCCUPIED

    def __str__(self):
        return str(self.value)

    def __cmp__(self, other):
        return self.value - other.value

    def __eq__(self, other):
        return self.x == other.x and self.y == other.y


class BeeType(Enum):
    SCOUT = 1
    ONLOOKER = 2
    EMPLOYED = 3

    def __str__(self):
        if self.value == 1:
            return 'scout'
        elif self.value == 2:
            return 'onlooker'
        else:
            return 'employed'


class Bee:
    def __init__(self, index: int = 0, x: float = 0.0, y: float = 0.0, type: BeeType = BeeType.SCOUT, decay: int = 3,
                 function_type: FunctionType = FunctionType.ROSENBROCK, search_pase: float = 0.1):
        self.index = index
        self.x = x
        self.y = y
        self.function_type = function_type
        self.search_pase = search_pase
        self.type = type
        self.food_source = FoodSource(self.x, self.y, function_type)
        self.decay = decay

    def get_found_food_source(self):
        return self.food_source

    def find_new_food_source(self):
        self.food_source.status = FoodSourceStatus.DEPLETED
        self.food_source = FoodSource(self.x, self.y, self.function_type)
        return self.food_source

    def __str__(self):
        return str(self.index) + '(' + str(self.type) + ')' + ': ' + str(self.x) + " " + str(self.y) + " -> " + str(
            self.food_source)

    def __eq__(self, other):
        return self.index == other.index

    def search(self, emp):
        u1 = random.randint(-1, 1)
        u2 = random.randint(-1, 1)
        new_x = emp.x + random.uniform(0, self.search_pase) * u1
        new_y = emp.y + random.uniform(0, self.search_pase) * u2
        return FoodSource(new_x, new_y, function_type=self.function_type)

    def search_scout(self, x_min, x_max, y_min, y_max):
        x = random.uniform(x_min, x_max)
        y = random.uniform(y_min, y_max)
        return FoodSource(x, y, function_type=self.function_type)


# ABC
def artificial_bee_colony(nr_albine, nr_iteratii, decay_rate, function_type):
    (x_min, x_max, y_min, y_max, mashgrid_rate) = get_max_and_min(function_type)
    plt.ion()
    food_sources = []
    emp = []
    onl = []
    sco = []
    # Initializam toate albinele ca fiind scout la inceput
    for i in range(nr_albine):
        sco.append(Bee(i, random.uniform(x_min, x_max), random.uniform(y_min, y_max), function_type=function_type, search_pase=mashgrid_rate))
    for i in range(nr_albine):
        food_sources.append(sco[i].food_source)
    # Sortam albinele scout dupa valoare sursei de hrana si jumatate din albine devin employed si jumatate onlooker
    sco.sort(key=operator.attrgetter('food_source.value'))
    best_food_source = sco[0].food_source
    for i in range(nr_albine):
        if i <= int(nr_albine / 2):
            sco[i].type = BeeType.EMPLOYED
            emp.append(sco[i])
        else:
            sco[i].type = BeeType.ONLOOKER
            onl.append(sco[i])
    sco.clear()
    prob = []
    fig = plt.figure()
    ax = axes3d.Axes3D(fig)
    # Incepem iteratiile
    for t in range(nr_iteratii):
        print('Iteratia ' + str(t))
        # Fiecare albina employed cauta un loc mai bun in vecinatatea s-a
        for i in range(len(emp)):
            new_food_source = emp[i].search(emp[i])
            if new_food_source not in food_sources:
                if new_food_source.value > emp[i].food_source.value:
                    old_food_source = emp[i].food_source
                    old_food_source.status = FoodSourceStatus.DEPLETED
                    food_sources.append(new_food_source)
                    emp[i].food_source = new_food_source
                    emp[i].x = new_food_source.x
                    emp[i].y = new_food_source.y
                    emp[i].decay = decay_rate
                else:
                    emp[i].decay = emp[i].decay - 1
        sum = 0
        for i in range(len(emp)):
            sum = sum + emp[i].food_source.value
        prob.clear()
        # Calculam probabilitatile pentru fiecare sursa de hrana gasita de albinele employed de a fi alese de un onlooker
        for i in range(len(emp)):
            prob.append(emp[i].food_source.value / sum)
        # Pentru fiecare onlooker
        for i in range(len(onl)):
            u = random.uniform(0, 1)
            index_emp = 0
            # Gasim un employed pe care sa il cerceteze
            for j in range(len(prob)):
                if j == 0:
                    if u <= prob[j] and u > 0:
                        index_emp = j
                else:
                    if u <= prob[j] and u > prob[j - 1]:
                        index_emp = j
            # Luam o sursa de hrana de pe langa o albina employed
            new_food_source = onl[i].search(emp[index_emp])
            # Daca e noua
            if new_food_source not in food_sources:
                # Mutam albina onlooker pe pozitia noua
                old_food_source = onl[i].food_source
                old_food_source.status = FoodSourceStatus.DEPLETED
                food_sources.append(new_food_source)
                onl[i].food_source = new_food_source
                onl[i].x = new_food_source.x
                onl[i].y = new_food_source.y
                onl[i].decay = decay_rate
        # Pentru fiecare employed
        for i in range(len(emp)):
            # Daca a epuizat hrana
            if emp[i].decay == 0:
                print('Employee ' + str(emp[i].index) + " has depleted it's food source")
                new_food_source = emp[i].search_scout(x_min, x_max, y_min, y_max)
                print(str(new_food_source))
                while new_food_source in food_sources:
                    print('Searching for ' + str(emp[i].index) + " new food source")
                    new_food_source = emp[i].search_scout(x_min, x_max, y_min, y_max)
                    print(str(new_food_source))
                food_sources.append(new_food_source)
                emp[i].x = new_food_source.x
                emp[i].y = new_food_source.y
                emp[i].type = BeeType.SCOUT
                emp[i].decay = decay_rate
                emp[i].food_source = new_food_source
        sco.clear()
        for i in range(len(emp)):
            sco.append(emp[i])
        for j in range(len(onl)):
            sco.append(onl[j])
        sco.sort(key=operator.attrgetter('food_source.value'))
        emp.clear()
        onl.clear()
        for i in range(nr_albine):
            if i <= int(nr_albine / 2):
                sco[i].type = BeeType.EMPLOYED
                emp.append(sco[i])
            else:
                sco[i].type = BeeType.ONLOOKER
                onl.append(sco[i])
        # Plotam rezultatele
        X = np.arange(x_min, x_max, mashgrid_rate)
        Y = np.arange(y_min, y_max, mashgrid_rate)
        X, Y = np.meshgrid(X, Y)
        Z = calc_function_np(X, Y, function_type)
        ax.plot_surface(X, Y, Z, rstride=1, cstride=1, cmap='hot')
        bee_x = [bee.x for bee in filter(lambda b: b.type == BeeType.EMPLOYED, sco)]
        bee_y = [bee.y for bee in filter(lambda b: b.type == BeeType.EMPLOYED, sco)]
        bee_z = [bee.food_source.value for bee in filter(lambda b: b.type == BeeType.EMPLOYED, sco)]
        bee_i = [bee.index for bee in filter(lambda b: b.type == BeeType.EMPLOYED, sco)]
        ax.plot(bee_x, bee_y, bee_z, 'ro')
        for i in range(len(bee_x)):
            plt.annotate(bee_i[i], (bee_x[i], bee_y[i]))
        bee_x = [bee.x for bee in filter(lambda b: b.type == BeeType.ONLOOKER, sco)]
        bee_y = [bee.y for bee in filter(lambda b: b.type == BeeType.ONLOOKER, sco)]
        bee_z = [bee.food_source.value for bee in filter(lambda b: b.type == BeeType.ONLOOKER, sco)]
        bee_i = [bee.index for bee in filter(lambda b: b.type == BeeType.ONLOOKER, sco)]
        ax.plot(bee_x, bee_y, bee_z, 'bo')
        for i in range(len(bee_x)):
            plt.annotate(bee_i[i], (bee_x[i], bee_y[i]))
        plt.xlabel('X')
        plt.ylabel('Y')
        plt.show()
        print('Pas ' + str(t))
        plt.pause(0.01)
        ax.clear()
    print('Bees: ')
    for i in range(len(emp)):
        print(str(emp[i]))
    for j in range(len(onl)):
        print(str(onl[j]))
    print('Food sources')
    food_sources.sort(key=operator.attrgetter('value'))
    for i in range(len(food_sources)):
        print(str(food_sources[i]))
    best_food_source = food_sources[0]
    print('Best food source is ')
    print('(' + str(best_food_source.x) + ' ' + str(best_food_source.y) + ') -> ' + str(best_food_source.value))
    plt.ioff()


artificial_bee_colony(100, 10, 3, function_type=FunctionType.GRIEWANK)
