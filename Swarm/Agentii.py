import time
import os

class Agent:

    def __init__(self, labirint, x, y):
        self.x = x
        self.y = y
        self.map = labirint

    def move(self):
        if self.has_not_vizited_space():
            self.map[self.x][self.y] = 'V'
        else:
            self.has_not_vizited_space()


    def has_not_vizited_space(self):
        has_not_vizited_space = False
        if self.map[self.x+1][self.y] == ' ':
            self.x = self.x+1
            has_not_vizited_space = True
        elif self.map[self.x-1][self.y] == ' ':
            self.x = self.x-1
            has_not_vizited_space = True
        elif self.map[self.x][self.y-1] == ' ':
            self.y = self.y-1
            has_not_vizited_space = True
        elif self.map[self.x][self.y+1] == ' ':
            self.y = self.y+1
            has_not_vizited_space = True
        return has_not_vizited_space

    def has_vizited_space(self):
        has_vizited_space = False
        if self.map[self.x+1][self.y] == 'V':
            self.x = self.x+1
            has_vizited_space = True
        elif self.map[self.x-1][self.y] == 'V':
            self.x = self.x-1
            has_vizited_space = True
        elif self.map[self.x][self.y-1] == 'V':
            self.y = self.y-1
            has_vizited_space = True
        elif self.map[self.x][self.y+1] == 'V':
            self.y = self.y+1
            has_vizited_space = True
        return has_vizited_space




def prepareLabirint(file_name):
    file = open(file_name, "r")
    lines = file.readlines()
    labirint = []
    xStart = 0
    yStart = 0
    for j in range(len(lines)):
        row = []
        for i in range(len(lines[j]) - 1):
            row.append(lines[j][i])
            if lines[j][i] == 'S':
                xStart = j
                yStart = i
        labirint.append(row)
    return (labirint,(xStart,yStart))

def showLabirint(labirint, agenti):
    os.system('cls')
    for i in range(len(labirint)):
        for j in range(len(labirint[i])):
            cellHasAgent = False;
            for a in agenti:
                if((a.x, a.y) == (i, j)):
                    print(str(str(agenti.index(a))+' '), sep=' ', end='', flush=True)
                    cellHasAgent = True
                    break
            if cellHasAgent == False:
                print(str(labirint[i][j])+' ', sep=' ', end='', flush=True)
        print()

def labirintIsDone(labirint):
    for i in range(len(labirint)):
        for j in range(len(labirint[i])):
            if(labirint[i][j] == " "):
                return False
    return True

def Labirint(nr_agenti, file_name):
    (labirint,(xStart, yStart)) = prepareLabirint(file_name=file_name)
    agenti = []
    for i in range(nr_agenti):
        agenti.append(Agent(labirint=labirint, x=xStart, y=yStart))
    showLabirint(labirint, agenti)
    while labirintIsDone(labirint) == False:
        for a in agenti:
            a.move()
        showLabirint(labirint, agenti)
        time.sleep(1)

Labirint(5, "input.txt")