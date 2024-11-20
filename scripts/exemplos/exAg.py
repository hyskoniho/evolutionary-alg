import sys
import numpy as np
from numpy import random
from typing import Final
import matplotlib.pyplot as plt


FRASE: Final[str] = 'EuAdoroInteligenciaArtificialPorqueTemMuitaMatematica'
TAM_CROMO: Final[int] = len(FRASE)
TAM_POP: Final[int] = TAM_CROMO*2


pop = np.zeros((TAM_POP, TAM_CROMO))
nova_pop = np.zeros((TAM_POP, TAM_CROMO))
pais = np.zeros((2, TAM_CROMO))
filhos = np.zeros((2, TAM_CROMO))
nota_pop = np.zeros((TAM_POP, 3))


def init_pop():
    global pop 
    pop = random.randint(low=65, high=122, size=(TAM_POP, TAM_CROMO))


def avalia_pop():
    global nota_pop
    soma_apt = 0
    for i in range(TAM_POP):

        apt = 0
        for j in range(TAM_CROMO):
            apt = apt + ((ord(FRASE[j]) - pop[i][j])**2)

        nota_pop[i][0] = i
        nota_pop[i][1] = apt
        nota_pop[i][2] = -1
        soma_apt = soma_apt + apt

    minsum = 0
    nota_pop = nota_pop[nota_pop[:, 1].argsort()]
    for i in range(TAM_POP):
        if(soma_apt > 0) and (nota_pop[i][1] > 0):
            nota_pop[i][2] = ((1 / nota_pop[i][1]) / soma_apt) * 100
        else:
            nota_pop[i][2] = 0
        minsum = minsum + nota_pop[i][2]

    for i in range(TAM_POP):
        if(minsum > 0):
            nota_pop[i][2] = nota_pop[i][2] / minsum
        else:
            nota_pop[i][2] = 0


def seleciona_pais():
    global pais
    r_pai1 = random.random_sample(size=None)
    r_pai2 = random.random_sample(size=None)

    acum = 0
    for i in range(TAM_POP):
        acum = acum + nota_pop[i][2]
        if(acum >= r_pai1):
            pais[0] = pop[nota_pop[i][0].astype(int)]
            break

    acum = 0
    for i in range(TAM_POP):
        acum = acum + nota_pop[i][2]
        if(acum >= r_pai2):
            pais[1] = pop[nota_pop[i][0].astype(int)]
            break


def cruza_pais():
    global filhos

    r_cruza = random.random_sample(size=None)
    if(r_cruza < 0.80):
        corte = random.randint(low=0, high=TAM_CROMO-1)   
        filhos[0][:corte] = pais[0][:corte]
        filhos[0][corte:] = pais[1][corte:]
        filhos[1][corte:] = pais[0][corte:]
        filhos[1][:corte] = pais[1][:corte]
    else:
        filhos[0] = pais[0]
        filhos[1] = pais[1]


def muta_filhos():
    global filhos

    for i in range(TAM_CROMO):
        r_muta = random.random_sample(size=None)
        if(r_muta < 0.03):
            filhos[0][i] = random.randint(low=65, high=122)

    for i in range(TAM_CROMO):
        r_muta = random.random_sample(size=None)
        if(r_muta < 0.03):
            filhos[1][i] = random.randint(low=65, high=122)


def elitismo(qtde):
    global nova_pop
    for i in range(qtde):
        nova_pop[i] = pop[nota_pop[i][0].astype(int)]


def imprime_pop():
    for i in range(len(FRASE)*2):
        for j in range(len(FRASE)):
            sys.stdout.write(chr(pop[i][j]))
        print("")


def imprime_nota_pop():
    acum = 0 
    for i in range(TAM_POP):
        acum = acum + nota_pop[i][2]
        print('Individuo: ', nota_pop[i][0], '- Nota: ', nota_pop[i][1], '- (%): ', nota_pop[i][2], ' - Acum: ', acum)

   
def imprime_melhor():
    sys.stdout.write('>> Melhor: ')
    for i in range(len(FRASE)):
        sys.stdout.write(chr(pop[nota_pop[0][0].astype(int)][i].astype(int)))
    print(' - Nota: ', nota_pop[0][1], ' - (%): ', nota_pop[0][2])


def imprime_pior():
    sys.stdout.write('>> Pior:   ')
    for i in range(len(FRASE)):
        sys.stdout.write(chr(pop[nota_pop[TAM_POP-1][0].astype(int)][i].astype(int)))
    print(' - Nota: ', nota_pop[TAM_POP-1][1], ' - (%): ', nota_pop[TAM_POP-1][2])


def imprime_medio():
    sys.stdout.write('>> Medio:  ')
    for i in range(len(FRASE)):
        sys.stdout.write(chr(pop[nota_pop[((TAM_POP - 1) // 2)][0].astype(int)][i].astype(int)))
    print(' - Nota: ', nota_pop[((TAM_POP - 1) // 2)][1], ' - (%): ', nota_pop[((TAM_POP - 1) // 2)][2])


if(__name__ == '__main__'):
    #listas para graficos
    geracao = []
    melhor = []
    pior = []
    medio = []

    print(FRASE)
    init_pop()
    imprime_pop()

    for i in range(2000):
        print('GERACAO: ', i)
        avalia_pop()

        imprime_melhor()
        imprime_pior()
        imprime_medio()

        #criterio de parada
        if(nota_pop[0][1] < 1):
            break

        #dados para graficos
        geracao.append(i)
        melhor.append(nota_pop[0][1])
        pior.append(nota_pop[TAM_POP-1][1])
        medio.append(nota_pop[(TAM_POP-1)//2][1])

        #preservar n melhores
        j = 4
        elitismo(j)

        #gerar nova populacao
        while(j < TAM_POP):
            seleciona_pais()
            cruza_pais()
            muta_filhos()
            nova_pop[j] = filhos[0]
            nova_pop[j+1] = filhos[1]
            j = j + 2

        pop = nova_pop.copy()
        nova_pop = np.zeros((TAM_POP, TAM_CROMO))


    plt.title("CONVERGENCIA AG")
    plt.plot(geracao, melhor, label = "Melhor")
    plt.plot(geracao, pior, label = "Pior")
    plt.plot(geracao, medio, label = "Medio")
    plt.legend()
    plt.show()

    imprime_melhor()
    imprime_pior()
    imprime_medio()
