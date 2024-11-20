import typing as tp
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd

# PCV
# Informacao heuristica = distancia

# cidades a serem visitadas
CIDADES: tp.Final[int] = 10

# constantes do ACO
A: tp.Final[float] = 0.5
B: tp.Final[float] = 0.5
R: tp.Final[float] = 0.5
Q: tp.Final[float] = 1.0

cidades = np.arange(CIDADES)
inicio = np.copy(cidades)
tours = np.empty((CIDADES, CIDADES+1))
custos = np.zeros(CIDADES)
melhor_agente = -1
distancia_cidades = np.array((CIDADES, CIDADES))
feromonios = np.empty((CIDADES, CIDADES))
qtde_feromonio = np.zeros(CIDADES)

# heurística do problema: distâncias
distancia_cidades = [
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

# mapa visual
mapa_cidades = np.array([
                         [2, 2], # 1
                         [2, 3], # 2
                         [3, 4], # 3
                         [4, 4], # 4
                         [5, 3], # 5
                         [5, 2], # 6
                         [5, 5], # 7
                         [5, 4], # 8
                         [4, 2], # 9
                         [2, 4], # 10                        
                         [2, 2] # volta inicio
                        ]) 

# feromonios iniciais
feromonios = [
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

# retorna cidade nova
def prox_cidade(_atual, _tour):
    prob = 0
    ind = _atual

    soma = 0
    for c in range(CIDADES):
        w = np.where(_tour == c)
        if(len(w[0]) == 0):
            soma = soma + ((1 / distancia_cidades[_atual][c]) * feromonios[_atual][c])

    for c in range(CIDADES):
        w = np.where(_tour == c)
        if(len(w[0]) == 0):
            if(prob == 0): 
                prob = (((1 / distancia_cidades[_atual][c]) * feromonios[_atual][c]) / soma)
                ind = c
            else:
                aux = (((1 / distancia_cidades[_atual][c]) * feromonios[_atual][c]) / soma)
                if(aux > prob):
                    prob = aux
                    ind = c
    return ind


# apura custos dos tours
def custos_tours():
    global custos
    global melhor_agente

    custos.fill(0)
    for f in range(CIDADES):
        for a in range(CIDADES):
            if((a+1) <= CIDADES):
                custos[f] = custos[f] + distancia_cidades[tours[f][a].astype(int)][tours[f][a+1].astype(int)]

    print(custos)

    melhor_agente = -1
    aux = 0
    for a in range(CIDADES):
        qtde_feromonio[a] = Q / custos[a]

        if(aux == 0):
            aux = custos[a] 
            melhor_agente = a
        else: 
            if(custos[a] < aux): 
                aux = custos[a]
                melhor_agente = a

    print(melhor_agente, tours[melhor_agente])


# depositar/evaporar feromonio
def atualiza_feromonio():
    global feromonios

    print(feromonios)

    # evaporar feromônios de todas as arestas
    for c1 in range(CIDADES):
        for c2 in range(CIDADES):
            if(c1 != c2): 
                feromonios[c1][c2] = (1 - R) * feromonios[c1][c2]

    print(feromonios)

    # checar quem tem as cidades (arestas) do tour do melhor agente e depositor feromonio
    for m in range(CIDADES+1): # cidades do melhor agente
        if(m+1 < CIDADES):
            for a in range(CIDADES): #todos os agentes
                for c in range(CIDADES): #cidades dos agentes
                    if(c+1 < CIDADES):
                        if((tours[melhor_agente][m+0].astype(int) == tours[a][c+0].astype(int) and tours[melhor_agente][m+1].astype(int) == tours[a][c+1].astype(int)) or \
                           (tours[melhor_agente][m+0].astype(int) == tours[a][c+1].astype(int) and tours[melhor_agente][m+1].astype(int) == tours[a][c+0].astype(int))):
                            feromonios[m+0][m+1] = feromonios[m+0][m+1] + qtde_feromonio[a]
                            feromonios[m+1][m+0] = feromonios[m+1][m+0] + qtde_feromonio[a]
            
    print(feromonios)



# iteracoes (epocas)
for i in range(3):
    tours.fill(-1)

    # cidade inicial para cada formiga
    np.random.shuffle(inicio)

    for f in range(CIDADES):        
        print("Formiga", f, "iniciando tour na cidade", inicio[f])

        # fazendo o tour
        t = 0
        tours[f][t] = inicio[f]
        while(True):
            t = t+1
            if(t < CIDADES):
                tours[f][t] = prox_cidade(tours[f][t-1].astype(int), tours[f])
            else:
                tours[f][t] = inicio[f]
                break
        
        print(tours[f])

    # apura custos dos tours
    custos_tours()

    # plotar todos os tours
    str = ['A','B','C','D','E','F','G','H','I', 'J']
    x, y = mapa_cidades.T
    plt.plot(x, y, color='black', marker='o', markersize=5)
    for i in range(CIDADES):
        plt.annotate(str[i], (x[i], y[i]), xytext=(x[i]+0.03, y[i]+0.1), bbox=dict(boxstyle="round", alpha=0.1), color="red", size=10, fontweight="bold")

    graph = np.empty((CIDADES+1, 2))
    for f in range(CIDADES):
        for c in range(CIDADES+1):
            graph[c] = mapa_cidades[tours[f][c].astype(int)]

        x, y = graph.T
        plt.plot(x, y, linestyle='dashed', color='green')

    # plotar melhor tour
    for c in range(CIDADES+1):
        graph[c] = mapa_cidades[tours[melhor_agente][c].astype(int)]

    x, y = graph.T
    #plt.ion()
    plt.plot(x, y, color='blue')
    #plt.draw()
    #plt.pause(0.005)
    plt.show()

    # atualiza feromonios
    atualiza_feromonio()
