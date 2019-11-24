from cidade import *
from VRP.vrp import VRP
import numpy as np

def lerEntrada(file):
    arq = open(file)
    
    texto = arq.readlines()
    texto = texto[6:]
    texto = texto[:len(texto) - 1]
    
    arq.close()
    return texto

# ARQ_ENTRADA = "./Dados/att532.tsp"

# arq = open(ARQ_ENTRADA)
# texto = arq.readlines()

# texto = texto[6:]
# texto = texto[:len(texto) - 1]

def getListaCidades(texto):

    lista_cidades = []

    for linha in texto:
        linha = linha.strip()
        aux = linha.split(' ')
        lista_cidades.append(Cidade(aux[0], float(aux[1]), float(aux[2])))

    return lista_cidades

def leEntradaVRP(nomeArquivo):
    vrp = VRP()
    
    with open(nomeArquivo, 'r') as f:
        linhas = f.readlines()
        name = linhas[0].strip().split(' : ')[1]
        comment = linhas[1].strip().split(' : ')[1:]
        vrpType = linhas[2].strip().split(' : ')[1]
        dimension = int(linhas[3].strip().split(' : ')[1])
        edge_weight_type = linhas[4].strip().split(' : ')[1]
        capacity = int(linhas[5].strip().split(' : ')[1])

        vrp.number_of_trucks = int(name.split('-')[2][1:])
        vrp.set_dimension(dimension)
        vrp.set_capacity(capacity)

        for i in range(dimension):
            linha = linhas[7 + i].strip().split(' ')
            vrp.append_node(np.array([float(linha[1]), float(linha[2])]))
            # print(np.array([float(linha[1]), float(linha[2])]))

        for i in range(dimension):
            linha = linhas[8 + dimension + i].strip().split(' ')
            vrp.append_demand(np.array([float(linha[1])]))

    return vrp        
