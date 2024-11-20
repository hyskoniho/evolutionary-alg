import sys
import numpy as np
from numpy import random
from typing import Final
import matplotlib.pyplot as plt

v00 = 65; v01 = 122; v03 = 2000; v04 = 1.00; v05 = 1.00
v06: Final[str] = 'UmaAvalicaoPraticadeAlgoritmoGeneticoemCinquentaMinutos'

v1: Final[int] = len(v06)
v2: Final[int] = v1*2

v3 = np.zeros((v2, v1))
v4 = np.zeros((v2, v1))
v6 = np.zeros((2, v1))
v7 = np.zeros((2, v1))
v8 = np.zeros((v2, 3))


def heraclito():
    global v7

    v15 = random.random_sample(size=None)
    if(v15 <= v04):
        v16 = random.randint(low=0, high=v1-1)   
        v7[0][:v16] = v6[0][:v16]
        v7[0][v16:] = v6[1][v16:]
        v7[1][v16:] = v6[0][v16:]
        v7[1][:v16] = v6[1][:v16]
    else:
        v7[0] = v6[0]
        v7[1] = v6[1]


def descartes(qtde):
    global v4
    for i in range(qtde):
        v4[i] = v3[v8[i][0].astype(int)]


def aristoteles():
    global v6
    v12 = random.random_sample(size=None)
    v13 = random.random_sample(size=None)

    v14 = 0
    for i in range(v2):
        v14 = v14 + v8[i][2]
        if(v14 >= v12):
            v6[0] = v3[v8[i][0].astype(int)]
            break

    v14 = 0
    for i in range(v2):
        v14 = v14 + v8[i][2]
        if(v14 >= v13):
            v6[1] = v3[v8[i][0].astype(int)]
            break


def platao():
    global v8
    v9 = 0
    for i in range(v2):

        v10 = 0
        for j in range(v1):
            v10 = v10 + ((ord(v06[j]) - v3[i][j])**2)

        v8[i][0] = i
        v8[i][1] = v10
        v8[i][2] = -1
        v9 = v9 + v10

    v11 = 0
    v8 = v8[v8[:, 1].argsort()]
    for i in range(v2):
        if(v9 > 0) and (v8[i][1] > 0):
            v8[i][2] = ((1 / v8[i][1]) / v9) * 100
        else:
            v8[i][2] = 0
        v11 = v11 + v8[i][2]

    for i in range(v2):
        if(v11 > 0):
            v8[i][2] = v8[i][2] / v11
        else:
            v8[i][2] = 0


def socrates():
    global v3 
    v3 = random.randint(low=v00, high=v01, size=(v2, v1))


def maquiavel():
    global v7

    for i in range(v1):
        v17 = random.random_sample(size=None)
        if(v17 <= v05):
            v7[0][i] = random.randint(low=v00, high=v01)

    for i in range(v1):
        v17 = random.random_sample(size=None)
        if(v17 <= v05):
            v7[1][i] = random.randint(low=v00, high=v01)


if(__name__ == '__main__'):
    socrates()

    for i in range(v03):
        platao()

        if(v8[0][1] < 1):
            break

        v18 = 4
        descartes(v18)

        while(v18 < v2):
            #filosófo 1 
            #filósofo 2
            #filósofo 3

            v4[v18] = v7[0]
            v4[v18+1] = v7[1]
            v18 = v18 + 2

        v3 = v4.copy()
        v4 = np.zeros((v2, v1))
