from genetic_algorithm import *
import utils as utils

def sensibilidade(lista_params,lista_cidades,v_inicial):
    num_individuos,num_geracoes,taxa_mutacao = lista_params
    melhores_param = [-1,-1,-1]
    resultados = ""
    melhor_fitness = 999999999
    distancias = matrix.calc_distances(lista_cidades)

    indice_vertice_inicial = utils.search_vertex_index(v_inicial, lista_cidades)

    arq = open('./resultados.txt', 'w')

    for ind in num_individuos:
        for ger in num_geracoes:
            for tx in taxa_mutacao:
                ag = AlgoritmoGenetico(ind)
                _,solucao = ag.resolver(tx, ger, distancias, indice_vertice_inicial)

                resultados += "Solucao: " + str(solucao) + " Ind: " + str(ind) + " Ger: " + str(ger) + " tx: " + str(tx) + "\n"

                if solucao < melhor_fitness:
                    melhor_fitness = solucao
                    melhores_param[0] = ind
                    melhores_param[1] = ger
                    melhores_param[2] = tx

                del ag
                
    arq.writelines(str(resultados))
    arq.close()

    return (melhores_param,melhor_fitness)


arq = "burma14.tsp"
l_params = ([50,250,1000],[20,150,400],[0.01,0.05,0.20])
lista_cidades = []
lista_cidades = getListaCidades(lerEntrada(arq))
print(lista_cidades)
params,fit = sensibilidade(l_params,lista_cidades,(7810,6053))

print(params)
print(fit)
