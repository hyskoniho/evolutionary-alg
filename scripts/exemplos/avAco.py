import typing as tp
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd

ESTRELAS: tp.Final[int] = 10

A: tp.Final[float] = 0.5
B: tp.Final[float] = 0.5
R: tp.Final[float] = 0.5
X: tp.Final[float] = 1.0

estrelas = np.arange(ESTRELAS)
caos = np.copy(estrelas)
odisseias = np.empty((ESTRELAS, ESTRELAS+1))
latinum = np.zeros(ESTRELAS)
o_volcano = -1
anos_luz = np.array((ESTRELAS, ESTRELAS))
asteroides = np.empty((ESTRELAS, ESTRELAS))
n_asteroides = np.zeros(ESTRELAS)

anos_luz = [
            [0.0, 1.0, 2.2, 2.0, 4.1, 5.0, 1.0, 2.2, 2.0, 4.1],
            [1.0, 0.0, 1.4, 2.2, 4.0, 5.0, 1.0, 2.2, 2.0, 4.1],
            [2.2, 1.4, 0.0, 2.2, 3.2, 5.0, 1.0, 2.2, 2.0, 4.1],
            [2.0, 2.2, 2.2, 0.0, 2.2, 5.0, 1.0, 2.2, 2.0, 4.1],
            [4.1, 4.0, 3.2, 2.2, 0.0, 5.0, 1.0, 2.2, 2.0, 4.1],
            [4.1, 4.0, 3.2, 2.2, 4.0, 0.0, 1.0, 2.2, 2.0, 4.1],
            [4.1, 4.0, 3.2, 2.2, 7.0, 5.0, 0.0, 2.2, 2.0, 4.1],
            [4.1, 4.0, 3.2, 2.2, 8.0, 5.0, 1.0, 0.0, 2.0, 4.1],
            [4.1, 4.0, 3.2, 2.2, 9.0, 5.0, 1.0, 2.2, 0.0, 4.1],
            [4.1, 4.0, 3.2, 2.2, 6.0, 5.0, 1.0, 2.2, 2.0, 0.0],
           ]

constelacoes = np.array([
                         [2, 2], 
                         [2, 3], 
                         [3, 4], 
                         [4, 4], 
                         [5, 3], 
                         [5, 2], 
                         [5, 5], 
                         [5, 4], 
                         [4, 2], 
                         [2, 4],                         
                         [2, 2] 
                        ]) 

asteroides = [
              [9.99, 0.30, 0.25, 0.20, 0.30, 0.30, 0.25, 0.20, 0.30, 0.20],
              [0.30, 9.99, 0.20, 0.20, 0.30, 0.30, 0.25, 0.20, 0.30, 0.20],
              [0.25, 0.20, 9.99, 0.10, 0.15, 0.30, 0.25, 0.20, 0.30, 0.20],
              [0.20, 0.20, 0.10, 9.99, 0.45, 0.30, 0.25, 0.20, 0.30, 0.20],
              [0.30, 0.30, 0.15, 0.45, 9.99, 0.30, 0.25, 0.20, 0.30, 0.20],
              [0.30, 0.30, 0.15, 0.45, 0.22, 9.99, 0.25, 0.20, 0.30, 0.20],
              [0.30, 0.30, 0.15, 0.45, 0.15, 0.30, 9.99, 0.20, 0.30, 0.20],
              [0.30, 0.30, 0.15, 0.45, 0.30, 0.30, 0.25, 9.99, 0.30, 0.20],
              [0.30, 0.30, 0.15, 0.45, 0.40, 0.30, 0.25, 0.20, 9.99, 0.20],
              [0.30, 0.30, 0.15, 0.45, 0.15, 0.30, 0.25, 0.20, 0.30, 9.99]
             ]

def __jornada(_x, _y):
    prob = 0
    ind = _x

    soma = 0
    for c in range(ESTRELAS):
        w = np.where(_y == c)
        if(len(w[0]) == 0):
            soma = soma + ((1 / anos_luz[_x][c]) * asteroides[_x][c])

    for c in range(ESTRELAS):
        w = np.where(_y == c)
        if(len(w[0]) == 0):
            if(prob == 0): 
                prob = (((1 / anos_luz[_x][c]) * asteroides[_x][c]) / soma)
                ind = c
            else:
                aux = (((1 / anos_luz[_x][c]) * asteroides[_x][c]) / soma)
                if(aux > prob):
                    prob = aux
                    ind = c
    return ind


def __odisseias():
    global latinum
    global o_volcano

    latinum.fill(0)
    for f in range(ESTRELAS):
        for a in range(ESTRELAS):
            if((a+1) <= ESTRELAS):
                latinum[f] = latinum[f] + anos_luz[odisseias[f][a].astype(int)][odisseias[f][a+1].astype(int)]

    print(latinum)

    o_volcano = -1
    aux = 0
    for a in range(ESTRELAS):
        n_asteroides[a] = X / latinum[a]

        if(aux == 0):
            aux = latinum[a] 
            o_volcano = a
        else: 
            if(latinum[a] < aux): 
                aux = latinum[a]
                o_volcano = a

    print(o_volcano, odisseias[o_volcano])


def __asteroides():
    global asteroides

    print(asteroides)

    for c1 in range(ESTRELAS):
        for c2 in range(ESTRELAS):
            if(c1 != c2): 
                asteroides[c1][c2] = (1 - R) * asteroides[c1][c2]

    print(asteroides)

    for m in range(ESTRELAS+1): 
        if(m+1 < ESTRELAS):
            for a in range(ESTRELAS): 
                for c in range(ESTRELAS): 
                    if(c+1 < ESTRELAS):
                        if((odisseias[o_volcano][m+0].astype(int) == odisseias[a][c+0].astype(int) and odisseias[o_volcano][m+1].astype(int) == odisseias[a][c+1].astype(int)) or \
                           (odisseias[o_volcano][m+0].astype(int) == odisseias[a][c+1].astype(int) and odisseias[o_volcano][m+1].astype(int) == odisseias[a][c+0].astype(int))):
                            asteroides[m+0][m+1] = asteroides[m+0][m+1] + n_asteroides[a]
                            asteroides[m+1][m+0] = asteroides[m+1][m+0] + n_asteroides[a]
            
    print(asteroides)


for i in range(3):
    odisseias.fill(-1)

    np.random.shuffle(caos)

    for v in range(ESTRELAS):        
        print("VOLCANO", v, "iniciando a odisseia ", caos[v])

        t = 0
        odisseias[v][t] = caos[v]
        while(True):
            t = t+1
            if(t < ESTRELAS):
                odisseias[v][t] = __jornada(odisseias[v][t-1].astype(int), odisseias[v])
            else:
                odisseias[v][t] = caos[v]
                break
        
        print(odisseias[v])

    __odisseias()
    __asteroides()
