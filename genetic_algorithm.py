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
            # print(self.pesos[self.cromossomo[i][j]])
            soma_pesos_caminhao += self.pesos[self.cromossomo[i][j]]

        return soma_pesos_caminhao

    def pode_levar_carga(self, i, peso_carga):
        # print(self.capacidade_ocupada(i) + peso_carga)
        if self.capacidade_ocupada(i) + peso_carga <= self.capacidade:
            return True

        return False

    def pode_realizar_troca(self, indice_caminhao_origem, indice_caminhao_destino, indice_carga_removida, indice_nova_carga):
        soma_pesos_caminhao = 0

        for j in range(len(self.cromossomo[indice_caminhao_origem])):
            # print(self.pesos[self.cromossomo[i][j]])
            soma_pesos_caminhao += self.pesos[self.cromossomo[indice_caminhao_origem][j]]

        soma_pesos_caminhao -= self.pesos[indice_carga_removida]

        if soma_pesos_caminhao + self.pesos[indice_nova_carga] <= self.capacidade:
            soma_pesos_caminhao = 0

            for j in range(len(self.cromossomo[indice_caminhao_destino])):
                # print(self.pesos[self.cromossomo[i][j]])
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
                    # soma_pesos_caminhao += math.trunc(distance.euclidean(origem, destino))
                    # soma_pesos_caminhao += self.pesos[self.cromossomo[i][j]][self.cromossomo[i][j+1]]

                origem = self.coordenadas[self.cromossomo[i][len(self.cromossomo[i]) - 1]]
                destino = self.coordenadas[0]
                soma_pesos_caminhao += distance.euclidean(origem, destino)

                soma_pesos_rota += math.trunc(soma_pesos_caminhao)
            
        self.custo_rota = soma_pesos_rota
        #Divido 1 pela distância pra ser a nota, já que quanto maior a distancia,
        #menor a nota
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

                        while indice_cromossomo_aleatorio == j or filho.pode_levar_carga(indice_cromossomo_aleatorio, self.pesos[indice]) == False:
                            indice_cromossomo_aleatorio = np.random.randint(len(filho.cromossomo))

                        filho.cromossomo[indice_cromossomo_aleatorio] = np.append(filho.cromossomo[indice_cromossomo_aleatorio], indice)

        return filho

    def gera_filho1(self, outro_individuo, geracao):
        parte1 = []
        parte2 = []

        for j in range(len(self.cromossomo)):
            # corte = round(rnd.random() * len(self.cromossomo[j]))
            if len(self.cromossomo[j]) > 0:
                corte = np.random.randint(len(self.cromossomo[j]))
            else:
                corte = 0

            parte1.append(self.cromossomo[j][:corte])
            parte2.append(outro_individuo.cromossomo[j])

            # print('corte')
            # print(corte)
            # print('parte 1')
            # print(parte1[j])
            # print('parte 2')
            # print(parte2[j])
            # print('menos')
            # print(list(set(parte2[j]) - set(parte1[j]) ))
            idx = sorted([np.where(parte2[j] == i) for i in list(set(parte2[j]) - set(parte1[j]) ) ])
            parte2[j] = np.array([parte2[j][i[0][0]] for i in idx])

        return self.gera_filho(geracao, parte1, parte2)

    def gera_filho2(self, outro_individuo, geracao):
        parte1 = []
        parte2 = []

        for j in range(len(self.cromossomo)):
            # corte = round(rnd.random() * len(self.cromossomo[j]))
            if len(self.cromossomo[j]) > 0:
                corte = np.random.randint(len(self.cromossomo[j]))
            else:
                corte = 0
                    
            parte1.append(outro_individuo.cromossomo[j][:corte])
            parte2.append(self.cromossomo[j])

            # print('corte')
            # print(corte)
            # print('parte 1')
            # print(parte1[j])
            # print('parte 2')
            # print(parte2[j])
            # print('menos')
            # print(list(set(parte2[j]) - set(parte1[j]) ))
            idx = sorted([np.where(parte2[j] == i) for i in list(set(parte2[j]) - set(parte1[j])  )])
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
        chance_mutacao = taxa_mutacao * len(self.coordenadas) * rnd.random()
        
        if rnd.random() < chance_mutacao:
            qtd_cromossomos_mutados = round(taxa_mutacao * len(self.coordenadas))
            # print(str(qtd_cromossomos_mutados) + ' mutacoes!')
            
            for _ in range(qtd_cromossomos_mutados):
                #-1 pra ignorar a primeira posicao e -1 já que começa de 0 e +1 para ignorar
                #a posicao 0
                indice_caminhao_origem = np.random.randint(len(self.cromossomo))

                while len(self.cromossomo[indice_caminhao_origem]) == 0:
                    indice_caminhao_origem = np.random.randint(len(self.cromossomo))

                # posicao1 = round(rnd.random() * (len(self.cromossomo[indice_caminhao_origem]) - 2)) + 1
                posicao1 = np.random.randint(len(self.cromossomo[indice_caminhao_origem]))

                indice_caminhao_destino = np.random.randint(len(self.cromossomo))

                while len(self.cromossomo[indice_caminhao_destino]) == 0:
                    indice_caminhao_destino = np.random.randint(len(self.cromossomo))

                # posicao2 = round(rnd.random() * (len(self.cromossomo[indice_caminhao_destino]) - 2)) + 1
                posicao2 = np.random.randint(len(self.cromossomo[indice_caminhao_destino])) 

                # print(self.cromossomo[indice_caminhao_origem])
                # print(posicao1)
                # print(self.cromossomo[indice_caminhao_destino])
                # print(posicao2)

                num_tentativas = 0
                while self.pode_realizar_troca(indice_caminhao_origem, indice_caminhao_destino, self.cromossomo[indice_caminhao_origem][posicao1], self.cromossomo[indice_caminhao_destino][posicao2]) == False:
                    indice_caminhao_destino = np.random.randint(len(self.cromossomo))

                    while len(self.cromossomo[indice_caminhao_destino]) == 0:
                        indice_caminhao_destino = np.random.randint(len(self.cromossomo))

                    # posicao2 = round(rnd.random() * (len(self.cromossomo[indice_caminhao_destino]) - 2)) + 1
                    posicao2 = np.random.randint(len(self.cromossomo[indice_caminhao_destino])) 
                    num_tentativas += 1

                    if num_tentativas > 50:
                        print('AGARRADO')
                        indice_caminhao_origem = np.random.randint(len(self.cromossomo))

                        while len(self.cromossomo[indice_caminhao_origem]) == 0:
                            indice_caminhao_origem = np.random.randint(len(self.cromossomo))
                        # posicao1 = round(rnd.random() * (len(self.cromossomo[indice_caminhao_origem]) - 2)) + 1
                        posicao1 = np.random.randint(len(self.cromossomo[indice_caminhao_origem]))
                        num_tentativas = 0

                    # print(self.cromossomo[indice_caminhao_origem])
                    # print(posicao1)
                    # print(self.cromossomo[indice_caminhao_destino])
                    # print(posicao2)
                    
                
                temp = self.cromossomo[indice_caminhao_origem][posicao1]
                self.cromossomo[indice_caminhao_origem][posicao1] = self.cromossomo[indice_caminhao_destino][posicao2]
                self.cromossomo[indice_caminhao_destino][posicao2] = temp
                
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

        
    #Temos que adaptar os parâmetros recebidos para os usados em nosso problema.
    def inicializa_populacao(self, coordenadas, pesos, capacidade, numero_caminhoes):
        for i in range(self.tamanho_populacao):
            self.populacao.append(Individuo(coordenadas, pesos, capacidade, numero_caminhoes))
            lista_indices = list(range(1, len(coordenadas)))

            # for j in range(numero_caminhoes):
            #     self.populacao[i].cromossomo.append(np.array([], dtype=int))

            while len(lista_indices) > 0:
                posicao = np.random.randint(len(lista_indices)) 
                j = np.random.randint(numero_caminhoes)

                # k = 0
                while self.populacao[i].pode_levar_carga(j, pesos[posicao]) == False:
                    j = np.random.randint(numero_caminhoes)

                    # if k == 20:
                    #     print('AGARRADO')
                    #     print(self.populacao[i].cromossomo)
                    #     print('-------')
                    # k += 1

                self.populacao[i].cromossomo[j] = np.append(self.populacao[i].cromossomo[j], lista_indices[posicao])
                lista_indices.pop(posicao)

                    # rnd.shuffle(self.populacao[i].cromossomo[i])
            
            # for j in range(len(self.populacao[i].cromossomo)):
            #     print('OI')
            #     self.populacao[i].cromossomo[j] = np.append(self.populacao[i].cromossomo[j], 0)
            #     print(self.populacao[i].cromossomo[j])
            
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

            # for i in range(len(individuo.cromossomo)):
            #     print(individuo.capacidade_ocupada(i))
            
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
    def resolver(self, taxa_mutacao, numero_geracoes, coordenadas, pesos, capacidade, numero_caminhoes):
        self.inicializa_populacao(coordenadas, pesos, capacidade, numero_caminhoes)
        
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
                                
                nova_populacao.append(filhos[0].mutacao(taxa_mutacao))
                nova_populacao.append(filhos[1].mutacao(taxa_mutacao))
                # nova_populacao.append(filhos[0])
                # nova_populacao.append(filhos[1])            
                
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
    tamanho_populacao = int(sys.argv[2])
    taxa_mutacao = float(sys.argv[3])
    numero_geracoes = int(sys.argv[4])
    numero_execucoes = int(sys.argv[5])
    pasta = sys.argv[6]
    
    print('Entrada: ' + entrada)

    vrp = leEntradaVRP(entrada)
    
    # entrada = "a280.tsp"
    # tamanho_populacao = 100
    # taxa_mutacao = 0.40
    # numero_geracoes = 1001
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
    
    # print('CUSTO MEDIO: ' + str(media_resultados))
    # print('MELHOR: ' + str(melhor_resultado))
    # print('PIOR: ' + str(pior_resultado))
    # print('DESVIO PADRAO: ' + str(desvio_padrao))
    # print('TEMPO MEDIO (s): ' + str(media_tempo))
