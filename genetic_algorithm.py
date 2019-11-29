import random as rnd
# import matplotlib.pyplot as plt
import numpy as numpy
import sys as sys
import math
import statistics

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
    def __init__(self, coordenadas, pesos, capacidade, numero_caminhoes, geracao = 1):
        self.pesos = pesos
        self.coordenadas = coordenadas
        self.capacidade = capacidade
        self.geracao = geracao
        self.custo_rota = 0
        self.nota_avaliacao = 0
        self.numero_caminhoes = numero_caminhoes
        self.cromossomo = []

        for _ in range(numero_caminhoes):
            self.cromossomo.append(np.array([], dtype=int))

    def capacidade_ocupada(self, i):
        soma_pesos_caminhao = 0

        for j in range(len(self.cromossomo[i])):
            soma_pesos_caminhao += self.pesos[self.cromossomo[i][j]]

        return soma_pesos_caminhao

    def pode_levar_carga(self, i, peso_carga):
        if self.capacidade_ocupada(i) + peso_carga <= self.capacidade:
            return True

        return False

    def pode_realizar_troca(self, indice_caminhao_origem, indice_caminhao_destino, indice_carga_removida, indice_nova_carga):
        soma_pesos_caminhao = 0

        for j in range(len(self.cromossomo[indice_caminhao_origem])):
            soma_pesos_caminhao += self.pesos[self.cromossomo[indice_caminhao_origem][j]]

        soma_pesos_caminhao -= self.pesos[indice_carga_removida]

        if soma_pesos_caminhao + self.pesos[indice_nova_carga] <= self.capacidade:
            soma_pesos_caminhao = 0

            for j in range(len(self.cromossomo[indice_caminhao_destino])):
                soma_pesos_caminhao += self.pesos[self.cromossomo[indice_caminhao_destino][j]]

            soma_pesos_caminhao -= self.pesos[indice_nova_carga]

            if soma_pesos_caminhao + self.pesos[indice_carga_removida] <= self.capacidade:
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

            if len(self.cromossomo[i]) > 0:
                origem = self.coordenadas[0]
                destino = self.coordenadas[self.cromossomo[i][0]]
                soma_pesos_caminhao += distance.euclidean(origem, destino)

                for j in range(len(self.cromossomo[i]) - 1):
                    origem = self.coordenadas[self.cromossomo[i][j]]
                    destino = self.coordenadas[self.cromossomo[i][j+1]]

                    soma_pesos_caminhao += distance.euclidean(origem, destino)

                origem = self.coordenadas[self.cromossomo[i][len(self.cromossomo[i]) - 1]]
                destino = self.coordenadas[0]
                soma_pesos_caminhao += distance.euclidean(origem, destino)

                soma_pesos_rota += math.trunc(soma_pesos_caminhao)
            
        self.custo_rota = soma_pesos_rota
        self.nota_avaliacao = 1 / soma_pesos_rota

    def gera_filho(self, geracao, parte1, parte2):
        filho = Individuo(self.coordenadas, self.pesos, self.capacidade, self.numero_caminhoes, geracao + 1)

        for j in range(len(self.cromossomo)):
            filho.cromossomo[j] = np.append(filho.cromossomo[j], parte1[j])

        for j in range(len(self.cromossomo)):
            for indice in parte2[j]:
                if filho.ja_possui_indice(indice) == False:
                    if filho.pode_levar_carga(j, self.pesos[indice]):
                        filho.cromossomo[j] = np.append(filho.cromossomo[j], indice)
                    else:
                        indice_cromossomo_aleatorio = np.random.randint(len(filho.cromossomo))

                        tentativas = 0
                        while indice_cromossomo_aleatorio == j or filho.pode_levar_carga(indice_cromossomo_aleatorio, self.pesos[indice]) == False:
                            indice_cromossomo_aleatorio = np.random.randint(len(filho.cromossomo))
                            tentativas += 1

                            if tentativas == 50:
                                return False

                        filho.cromossomo[indice_cromossomo_aleatorio] = np.append(filho.cromossomo[indice_cromossomo_aleatorio], indice)

        return filho

    def gera_filho1(self, outro_individuo, geracao):
        filho = False

        while filho == False:
            parte1 = []
            parte2 = []

            for j in range(len(self.cromossomo)):
                if len(self.cromossomo[j]) > 0:
                    corte = np.random.randint(len(self.cromossomo[j]))
                else:
                    corte = 0

                parte1.append(self.cromossomo[j][:corte])
                parte2.append(outro_individuo.cromossomo[j])

                idx = sorted([np.where(parte2[j] == i) for i in list(set(parte2[j]) - set(parte1[j]) ) ])
                parte2[j] = np.array([parte2[j][i[0][0]] for i in idx])

            filho = self.gera_filho(geracao, parte1, parte2)
            
        return filho


    def gera_filho2(self, outro_individuo, geracao):
        filho = False

        while filho == False:
            parte1 = []
            parte2 = []

            for j in range(len(self.cromossomo)):
                if len(self.cromossomo[j]) > 0:
                    corte = np.random.randint(len(self.cromossomo[j]))
                else:
                    corte = 0
                        
                parte1.append(outro_individuo.cromossomo[j][:corte])
                parte2.append(self.cromossomo[j])

                idx = sorted([np.where(parte2[j] == i) for i in list(set(parte2[j]) - set(parte1[j])  )])
                parte2[j] = np.array([parte2[j][i[0][0]] for i in idx])

            filho = self.gera_filho(geracao, parte1, parte2)
            
        return filho

    def crossover(self, outro_individuo, geracao):
        filhos = [self.gera_filho1(outro_individuo, geracao),
                  self.gera_filho2(outro_individuo, geracao)]
        
        return filhos
    
    def mutacao(self, taxa_mutacao):      
        chance_mutacao = taxa_mutacao * len(self.coordenadas) * rnd.random()
        
        if rnd.random() < chance_mutacao:
            qtd_cromossomos_mutados = round(taxa_mutacao * len(self.coordenadas))
            
            for _ in range(qtd_cromossomos_mutados):
                indice_caminhao_origem = np.random.randint(len(self.cromossomo))

                while len(self.cromossomo[indice_caminhao_origem]) == 0:
                    indice_caminhao_origem = np.random.randint(len(self.cromossomo))

                posicao1 = np.random.randint(len(self.cromossomo[indice_caminhao_origem]))

                indice_caminhao_destino = np.random.randint(len(self.cromossomo))

                while len(self.cromossomo[indice_caminhao_destino]) == 0:
                    indice_caminhao_destino = np.random.randint(len(self.cromossomo))

                posicao2 = np.random.randint(len(self.cromossomo[indice_caminhao_destino])) 

                tentativas = 0
                while self.pode_realizar_troca(indice_caminhao_origem, indice_caminhao_destino, self.cromossomo[indice_caminhao_origem][posicao1], self.cromossomo[indice_caminhao_destino][posicao2]) == False:
                    indice_caminhao_destino = np.random.randint(len(self.cromossomo))

                    while len(self.cromossomo[indice_caminhao_destino]) == 0:
                        indice_caminhao_destino = np.random.randint(len(self.cromossomo))

                    posicao2 = np.random.randint(len(self.cromossomo[indice_caminhao_destino])) 

                    indice_caminhao_origem = np.random.randint(len(self.cromossomo))

                    while len(self.cromossomo[indice_caminhao_origem]) == 0:
                        indice_caminhao_origem = np.random.randint(len(self.cromossomo))
                    posicao1 = np.random.randint(len(self.cromossomo[indice_caminhao_origem]))
                    
                    tentativas += 1

                    if tentativas == 75:
                        break
                
                if tentativas < 75:
                    temp = self.cromossomo[indice_caminhao_origem][posicao1]
                    self.cromossomo[indice_caminhao_origem][posicao1] = self.cromossomo[indice_caminhao_destino][posicao2]
                    self.cromossomo[indice_caminhao_destino][posicao2] = temp
                
        return self
    
class AlgoritmoGenetico():
    def __init__(self, tamanho_populacao):
        self.tamanho_populacao = tamanho_populacao
        self.populacao = []
        self.geracao = 0
        self.melhor_solucao = 0
        self.soma_avaliacao = 0
        self.lista_solucoes = []
        self.peso_melhor_solucao = 0

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

        
    def inicializa_populacao(self, coordenadas, pesos, capacidade, numero_caminhoes):
        i = 0
        while i < self.tamanho_populacao:
            self.populacao.append(Individuo(coordenadas, pesos, capacidade, numero_caminhoes))
            lista_indices = list(range(1, len(coordenadas)))
            deu_problema = False

            while len(lista_indices) > 0:
                posicao = np.random.randint(len(lista_indices)) 
                j = np.random.randint(numero_caminhoes)

                tentativas = 0
                while self.populacao[i].pode_levar_carga(j, pesos[posicao]) == False:
                    j = np.random.randint(numero_caminhoes)

                    tentativas += 1

                    if tentativas == 75:
                        deu_problema = True
                        break

                if deu_problema == False:
                    self.populacao[i].cromossomo[j] = np.append(self.populacao[i].cromossomo[j], lista_indices[posicao])
                    lista_indices.pop(posicao)
                else:
                    break

            if deu_problema == False:
                i += 1
            else:
                self.populacao.pop()
            
        self.melhor_solucao = self.populacao[0]
        
    def ordena_populacao(self):
        self.populacao = sorted(self.populacao,
                                key = lambda populacao: populacao.nota_avaliacao,
                                reverse = True)
        
    def melhor_individuo(self, individuo):
        if individuo.nota_avaliacao > self.melhor_solucao.nota_avaliacao:
            self.melhor_solucao = individuo

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
    def resolver(self, taxa_mutacao, numero_geracoes, coordenadas, pesos, capacidade, numero_caminhoes):
        self.inicializa_populacao(coordenadas, pesos, capacidade, numero_caminhoes)
        
        for individuo in self.populacao:
            individuo.avaliacao()
            self.soma_avaliacao += individuo.nota_avaliacao

        self.ordena_populacao()
        
        self.melhor_solucao = self.populacao[0]
        self.lista_solucoes.append(self.melhor_solucao.custo_rota)

        print(self.melhor_solucao.custo_rota)
        self.geracao += 1
        
        for geracao in range(numero_geracoes):
            nova_populacao = []
             
            for individuos_gerados in range(0, self.tamanho_populacao, 2):                 
                pai1 = self.seleciona_pai(self.soma_avaliacao)
                pai2 = self.seleciona_pai(self.soma_avaliacao)
                
                while pai1 == pai2:
                    pai2 = self.seleciona_pai(self.soma_avaliacao)                    

                filhos = self.populacao[pai1].crossover(self.populacao[pai2], self.geracao)

                nova_populacao.append(filhos[0].mutacao(taxa_mutacao))
                nova_populacao.append(filhos[1].mutacao(taxa_mutacao))     
                
            individuos_mantidos = self.populacao[:round(self.tamanho_populacao * 0.10)]
                
            self.populacao = list(nova_populacao) + individuos_mantidos
            
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
            
        self.visualiza_geracao()
        print("Cromossomo: %s" % self.melhor_solucao.cromossomo)
        
        return (self.melhor_solucao.cromossomo,self.melhor_solucao.custo_rota)

def escreve_saida_csv(arquivo_saida, media_resultados, melhor_resultado, pior_resultado, desvio_padrao, media_tempo):
    with open(arquivo_saida, 'w') as f:
        f.write(str(media_resultados) + ';')
        f.write(str(melhor_resultado) + ';')
        f.write(str(pior_resultado) + ';')
        f.write(str(desvio_padrao) + ';')
        f.write(str(media_tempo) + '\n')

def escreve_saida_txt(arquivo_saida, media_resultados, melhor_resultado, pior_resultado, desvio_padrao, media_tempo):
    with open(arquivo_saida, 'w') as f:
        f.write('CUSTO MEDIO: ' + str(media_resultados) + '\n')
        f.write('MELHOR: ' + str(melhor_resultado) + '\n')
        f.write('PIOR: ' + str(pior_resultado) + '\n')
        f.write('DESVIO PADRAO: ' + str(desvio_padrao) + '\n')
        f.write('TEMPO MEDIO (s): ' + str(media_tempo) + '\n')

def escreve_resultado(pasta, arquivo_entrada, media_resultados, melhor_resultado, pior_resultado, desvio_padrao, media_tempo):
    nome = arquivo_entrada.split('/')[-1].split('.')[0]
    nome_saida_csv = pasta + '/' + nome + '.csv'
    nome_saida_txt = pasta + '/' + nome + '.txt'

    escreve_saida_csv(nome_saida_csv, media_resultados, melhor_resultado, pior_resultado, desvio_padrao, media_tempo)
    escreve_saida_txt(nome_saida_txt, media_resultados, melhor_resultado, pior_resultado, desvio_padrao, media_tempo)


if __name__ == '__main__':
    entrada = sys.argv[1]
    tamanho_populacao = int(sys.argv[2])
    taxa_mutacao = float(sys.argv[3])
    numero_geracoes = int(sys.argv[4])
    numero_execucoes = int(sys.argv[5])
    pasta = sys.argv[6]
    
    vrp = leEntradaVRP(entrada)
    resultados = []
    tempos = []

    for i in range(numero_execucoes):
        print('Execucao: ' + str(i))

        inicio = time.time()

        ag = AlgoritmoGenetico(tamanho_populacao)
        resultado = ag.resolver(taxa_mutacao, numero_geracoes, vrp.nodes, vrp.demands, vrp.get_capacity(), vrp.number_of_trucks)
        resultados.append(resultado)

        fim = time.time()
        tempos.append(fim - inicio)

    media_resultados = sum(resultado[1] for resultado in resultados) / float(numero_execucoes)
    melhor_resultado = min(resultado[1] for resultado in resultados)
    pior_resultado = max(resultado[1] for resultado in resultados)
    desvio_padrao = statistics.pstdev(resultado[1] for resultado in resultados)

    media_tempo = sum(tempos) / float(numero_execucoes)

    escreve_resultado(pasta, entrada, media_resultados, melhor_resultado, pior_resultado, desvio_padrao, media_tempo)
    
