import random as rnd
# import matplotlib.pyplot as plt
import numpy as numpy
import sys as sys
import math

import time as time

from cidade import *
from leitura import *
from Utils import matrix as matrix
from Utils import utils as utils
from scipy.spatial import distance

#Classe apenas para armazenar os dados que serão usados
class Produto():
    def __init__(self, nome, espaco, valor):
        self.nome = nome
        self.espaco = espaco
        self.valor = valor
        
#Classe que representa cada solução gerada. Ela que precisamos mudar.
#Neste problema nós procuramos os produtos a serem levados em um caminhão de
#espaço limitado de forma a maximizar o lucro.
class Individuo():
    def __init__(self, coordenadas, pesos, capacidade, indice_vertice_inicial, numero_caminhoes, geracao = 1):
        self.pesos = pesos
        self.coordenadas = coordenadas
        self.capacidade = capacidade
        self.geracao = geracao
        self.custo_rota = 0
        self.nota_avaliacao = 0
        self.indice_vertice_inicial = indice_vertice_inicial
        self.numero_caminhoes = numero_caminhoes
        self.cromossomo = []

        for _ in range(numero_caminhoes):
            self.cromossomo.append(np.array([], dtype=int))

    def capacidade_ocupada(self, i):
        soma_pesos_caminhao = 0

        for j in range(len(self.cromossomo[i])):
            # print(self.pesos[self.cromossomo[i][j]])
            soma_pesos_caminhao += self.pesos[self.cromossomo[i][j]]

        return soma_pesos_caminhao

    def pode_levar_carga(self, i, peso_carga):
        # print(self.capacidade_ocupada(i) + peso_carga)
        if self.capacidade_ocupada(i) + peso_carga <= self.capacidade:
            return True

        return False

    def ja_possui_indice(self, indice):
        for i in range(len(self.cromossomo)):
            for j in range(len(self.cromossomo[i])):
                if self.cromossomo[i][j] == indice:
                    return True

        return False
                
    #Função que vai atribuir uma nota pra solução gerada.
    def avaliacao(self):
        soma_pesos_rota = 0
        
        for i in range(len(self.cromossomo)):
            soma_pesos_caminhao = 0

            for j in range(len(self.cromossomo[i]) - 1):
                origem = self.coordenadas[self.cromossomo[i][j]]
                destino = self.coordenadas[self.cromossomo[i][j+1]]

                soma_pesos_caminhao += math.trunc(distance.euclidean(origem, destino))
                # soma_pesos_caminhao += self.pesos[self.cromossomo[i][j]][self.cromossomo[i][j+1]]

            soma_pesos_rota += soma_pesos_caminhao
            
        self.custo_rota = soma_pesos_rota
        #Divido 1 pela distância pra ser a nota, já que quanto maior a distancia,
        #menor a nota
        self.nota_avaliacao = 1 / soma_pesos_rota

    def gera_filho(self, geracao, parte1, parte2):
        filho = Individuo(self.coordenadas, self.pesos, self.capacidade, self.indice_vertice_inicial, self.numero_caminhoes, geracao + 1)

        for j in range(len(self.cromossomo)):
            filho.cromossomo[j] = np.append(filho.cromossomo[j], parte1[j])

        for j in range(len(self.cromossomo)):
            for indice in parte2[j]:
                if filho.ja_possui_indice(indice) == False:
                    if filho.pode_levar_carga(j, self.pesos[indice]):
                        filho.cromossomo[j] = np.append(filho.cromossomo[j], indice)
                    else:
                        indice_cromossomo_aleatorio = np.random.randint(len(filho.cromossomo))

                        while indice_cromossomo_aleatorio == j or filho.pode_levar_carga(indice_cromossomo_aleatorio, self.pesos[indice]) == False:
                            indice_cromossomo_aleatorio = np.random.randint(len(filho.cromossomo))

                        filho.cromossomo[indice_cromossomo_aleatorio] = np.append(filho.cromossomo[indice_cromossomo_aleatorio], indice)

        return filho

    def gera_filho1(self, outro_individuo, geracao):
        parte1 = []
        parte2 = []

        for j in range(len(self.cromossomo)):
            corte = round(rnd.random() * len(self.cromossomo[j]))
                    
            parte1.append(self.cromossomo[j][:corte])
            parte2.append(outro_individuo.cromossomo[j])

            idx = sorted([np.where(parte2[j] == i) for i in list(set(parte2[j]) - set(parte1[j]))])
            parte2[j] = np.array([parte2[j][i[0][0]] for i in idx])

        return self.gera_filho(geracao, parte1, parte2)

    def gera_filho2(self, outro_individuo, geracao):
        parte1 = []
        parte2 = []

        for j in range(len(self.cromossomo)):
            corte = round(rnd.random() * len(self.cromossomo[j]))
                    
            parte1.append(outro_individuo.cromossomo[j][:corte])
            parte2.append(self.cromossomo[j])

            idx = sorted([np.where(parte2[j] == i) for i in list(set(parte2[j]) - set(parte1[j]))])
            parte2[j] = np.array([parte2[j][i[0][0]] for i in idx])

        return self.gera_filho(geracao, parte1, parte2)

    #Algoritmo usado: Ordered Crossover
    def crossover(self, outro_individuo, geracao):
        filhos = [self.gera_filho1(outro_individuo, geracao),
                  self.gera_filho2(outro_individuo, geracao)]
        
        return filhos
    
    #Função que pode modificar cada gene. O gene só será modificado se o valor 
    #gerado aleatóriamente for maior que a taxa de mutação.
    #Se ocorrer mutação, troca a posição de 2 genes
    def mutacao(self, taxa_mutacao):      
        #Não pode haver mutação no vértice inicial       
        chance_mutacao = taxa_mutacao * len(self.cromossomo) * rnd.random()
        
        if rnd.random() < chance_mutacao:
            qtd_cromossomos_mutados = round(taxa_mutacao * len(self.cromossomo))
            
            for i in range(qtd_cromossomos_mutados):
                #-1 pra ignorar a primeira posicao e -1 já que começa de 0 e +1 para ignorar
                #a posicao 0
                posicao1 = round(rnd.random() * (len(self.cromossomo) - 2)) + 1
                posicao2 = round(rnd.random() * (len(self.cromossomo) - 2)) + 1
                
                temp = self.cromossomo[posicao1]
                self.cromossomo[posicao1] = self.cromossomo[posicao2]
                self.cromossomo[posicao2] = temp
                
        return self
    
#Classe que vai gerenciar todo o procedimento do algoritmo genetico. Acredito 
#que a única coisa que vai precisar mudar nela é a função que inicializa a 
#população.
class AlgoritmoGenetico():
    def __init__(self, tamanho_populacao):
        self.tamanho_populacao = tamanho_populacao
        self.populacao = []
        self.geracao = 0
        self.melhor_solucao = 0
        self.soma_avaliacao = 0
        self.lista_solucoes = []

    def escolhe_coordenadas_aleatorias(self, lista_indices, pesos, capacidade):
        indices_escolhidos = []
        capacidade_ocupada = 0
        num_max_coordenadas = np.random.randint(int(len(lista_indices) / 2))

        for _ in range(len(pesos)):
            posicao = np.random.randint(len(lista_indices))

            if capacidade_ocupada + pesos[posicao] <= capacidade:
                indices_escolhidos.append(lista_indices[posicao])
                capacidade_ocupada += pesos[posicao]
                lista_indices.pop(posicao)
            
                if capacidade_ocupada == capacidade or len(lista_indices) == 0 or len(indices_escolhidos) >= num_max_coordenadas:
                    return indices_escolhidos

        return indices_escolhidos

        
    #Temos que adaptar os parâmetros recebidos para os usados em nosso problema.
    def inicializa_populacao(self, coordenadas, pesos, capacidade, indice_vertice_inicial, numero_caminhoes):
        for i in range(self.tamanho_populacao):
            self.populacao.append(Individuo(coordenadas, pesos, capacidade, indice_vertice_inicial, numero_caminhoes))
            lista_indices = list(range(len(coordenadas)))

            # for j in range(numero_caminhoes):
            #     self.populacao[i].cromossomo.append(np.array([], dtype=int))

            while len(lista_indices) > 0:
                posicao = np.random.randint(len(lista_indices))
                j = np.random.randint(numero_caminhoes)

                k = 0
                while self.populacao[i].pode_levar_carga(j, pesos[posicao]) == False:
                    j = np.random.randint(numero_caminhoes)

                    if k == 20:
                        print('AGARRADO')
                        print(self.populacao[i].cromossomo)
                        print('-------')
                    k += 1

                self.populacao[i].cromossomo[j] = np.append(self.populacao[i].cromossomo[j], lista_indices[posicao])
                lista_indices.pop(posicao)

                    # rnd.shuffle(self.populacao[i].cromossomo[i])
            
            #Colocar o vértice inicial na posição 0
            # for j in range(len(self.populacao[i].cromossomo)):
            #     if self.populacao[i].cromossomo[j] == indice_vertice_inicial:
            #         temp = self.populacao[i].cromossomo[0]
            #         self.populacao[i].cromossomo[0] = indice_vertice_inicial
            #         self.populacao[i].cromossomo[j] = temp
                    
            #         break

            # soma = 0
            # for k in range(len(self.populacao[i].cromossomo)):
            #     soma += len(self.populacao[i].cromossomo[k])

            # print(soma)
            # print(self.populacao[i].cromossomo)
            # print('-------')
            
        self.melhor_solucao = self.populacao[0]
        
    def ordena_populacao(self):
        self.populacao = sorted(self.populacao,
                                key = lambda populacao: populacao.nota_avaliacao,
                                reverse = True)
        
    def melhor_individuo(self, individuo):
        if individuo.nota_avaliacao > self.melhor_solucao.nota_avaliacao:
            self.melhor_solucao = individuo
            
    #Soma as avaliações dos individuos da geração. É necessária na hora de 
    #selecionar o pai.
    def soma_avaliacoes(self):
        soma = 0
        
        for individuo in self.populacao:
            soma += individuo.nota_avaliacao
            
        return soma
    
    #Seleciona o pai usando o método da roleta viciada.
    def seleciona_pai(self, soma_avaliacao):
        pai = -1
        valor_sorteado = rnd.random() * soma_avaliacao
        soma = 0
        i = 0
        
        while i < len(self.populacao) and soma < valor_sorteado:
            soma += self.populacao[i].nota_avaliacao
            pai += 1
            i += 1
            
        return pai   
    
    #Função apenas pra printar os resultados de cada geração.
    def visualiza_geracao(self):
        print("\nGeracao atual: %s | Melhor solução -> G:%s -> Distancia: %s" % (self.geracao, 
                                                               self.melhor_solucao.geracao,
                                                               self.melhor_solucao.custo_rota))
        
    #Gerencia o funcionamento do algoritmo genético.
    def resolver(self, taxa_mutacao, numero_geracoes, coordenadas, pesos, capacidade, indice_vertice_inicial, numero_caminhoes):
        self.inicializa_populacao(coordenadas, pesos, capacidade, indice_vertice_inicial, numero_caminhoes)
        
        for individuo in self.populacao:
            individuo.avaliacao()
            self.soma_avaliacao += individuo.nota_avaliacao

        self.ordena_populacao()
        
        self.melhor_solucao = self.populacao[0]
        self.lista_solucoes.append(self.melhor_solucao.custo_rota)

        print('-----MELHOR-----')
        print(self.melhor_solucao.custo_rota)

        #self.visualiza_geracao()

        self.geracao += 1
        
        for geracao in range(numero_geracoes):
            #soma_avaliacao = self.soma_avaliacoes()
            nova_populacao = []
             
            for individuos_gerados in range(0, self.tamanho_populacao, 2):                 
                pai1 = self.seleciona_pai(self.soma_avaliacao)
                pai2 = self.seleciona_pai(self.soma_avaliacao)
                
                while pai1 == pai2:
                    pai2 = self.seleciona_pai(self.soma_avaliacao)                    
                
                filhos = self.populacao[pai1].crossover(self.populacao[pai2], self.geracao)
                                
                # nova_populacao.append(filhos[0].mutacao(taxa_mutacao))
                # nova_populacao.append(filhos[1].mutacao(taxa_mutacao))
                nova_populacao.append(filhos[0])
                nova_populacao.append(filhos[1])            
                
            individuos_mantidos = self.populacao[:round(self.tamanho_populacao * 0.10)]
                
            self.populacao = list(nova_populacao) + individuos_mantidos
            
            #print("Soma avaliacao: %s" % self.soma_avaliacao)
            self.soma_avaliacao = 0
            
            for individuo in self.populacao:
                individuo.avaliacao()
                self.soma_avaliacao += individuo.nota_avaliacao
                
            self.ordena_populacao()

            self.populacao = self.populacao[:self.tamanho_populacao]

            if geracao % 100 == 0:    
                self.visualiza_geracao()

            self.geracao += 1
            
            melhor = self.populacao[0]
            self.lista_solucoes.append(melhor.custo_rota)
            self.melhor_individuo(melhor)
            
            #print("Proximo ciclo")
            
        self.visualiza_geracao()
        print("Cromossomo: %s" % self.melhor_solucao.cromossomo)
        
        return (self.melhor_solucao.cromossomo,self.melhor_solucao.custo_rota)
            
    
#Apenas cria a lista de produtos que serão usados, chama a função que executa
#o algoritmo genético, printa o resultado e printa o gráfico.
if __name__ == '__main__':
    #agrv[1]: caminho dados
    #argv[2]: ponto x V_inicial
    #argv[3]: ponto y V_inicial
    #argv[4]: tamanho pop
    #argv[5]: tx mutacao
    #argv[6]: num geracoes
    entrada = sys.argv[1]
    vrp = leEntradaVRP(entrada)
    
    # print(vrp.nodes)
    # print(vrp.demands)
    print(vrp.number_of_trucks)

    # exit()
    lista_cidades = []
    
    entrada = "a280.tsp"
    vertice_inicial = (288, 149)
    tamanho_populacao = 20
    taxa_mutacao = 0.025
    numero_geracoes = 201
    
    lista_cidades = getListaCidades(lerEntrada(entrada))

    pesos = matrix.calc_distances(lista_cidades)
    
    '''
    lista_cidades = getListaCidades(lerEntrada(sys.argv[1]))

    pesos = matrix.calc_distances(lista_cidades)
    
    tamanho_populacao = int(sys.argv[4])
    taxa_mutacao = float(sys.argv[5])
    numero_geracoes = int(sys.argv[6])
    vertice_inicial = (float(sys.argv[2]), float(sys.argv[3]))

    print("x: %s  y: %s" % (sys.argv[2], sys.argv[3]))
    '''
    
    print(lista_cidades[0].x, lista_cidades[0].y)
    ag = AlgoritmoGenetico(tamanho_populacao)
    indice_vertice_inicial = 0

    resultado = ag.resolver(taxa_mutacao, numero_geracoes, vrp.nodes, vrp.demands, vrp.get_capacity(), indice_vertice_inicial, vrp.number_of_trucks)
        

    

