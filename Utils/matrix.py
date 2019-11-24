import numpy as numpy

def calc_distances(lista_cidades):
    A = numpy.zeros((len(lista_cidades), len(lista_cidades)))
    
    for i in range(len(lista_cidades)):
        for j in range(len(lista_cidades)):
            A[i][j] = numpy.linalg.norm(numpy.array((lista_cidades[i].x, lista_cidades[i].y)) 
            - numpy.array((lista_cidades[j].x, lista_cidades[j].y)))
            
    return A