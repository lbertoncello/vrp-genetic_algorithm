def char_search(char, l):
    for e in l:
        if e == char:
            return True
        
    return False

def search_vertex_index(v, lista_cidades):
    for i in range(len(lista_cidades)):
        if (lista_cidades[i].x, lista_cidades[i].y) == v:
            print(v)
            return i
        
    print(v)
    return -1

def distance(matrix, solucao):
    soma = 0

    for i in range(len(solucao) - 1):
        soma += matrix[solucao[i]][solucao[i + 1]]

    return soma