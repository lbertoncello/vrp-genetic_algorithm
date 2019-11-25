from leitura import *
import math
from scipy.spatial import distance

vrp = leEntradaVRP('../instancias-solucoes/Instancias/A/A-n32-k5.vrp')

solucoes = [np.array([[98., 14.],
       [98.,  5.],
       [93.,  3.],
       [91.,  2.],
       [84., 25.],
       [84., 39.],
       [80., 55.]]), np.array([[98., 52.],
       [96., 44.],
       [88., 51.],
       [85., 60.]]), np.array([[57., 69.],
       [61., 62.]]), np.array([[20., 70.],
       [19., 32.],
       [14., 24.],
       [ 2., 39.],
       [ 5., 42.],
       [ 1., 65.],
       [ 3., 82.],
       [ 9., 97.],
       [29., 89.],
       [50., 93.]]), np.array([[61., 59.],
       [23., 15.],
       [ 5., 10.],
       [13.,  7.],
       [42.,  9.],
       [49.,  8.],
       [50.,  5.],
       [58., 30.]])]

def avaliacao(vrp, solucoes):
    soma_pesos_rota = 0
    
    for i in range(len(solucoes)):
        soma_pesos_caminhao = 0

        origem = vrp.nodes[0]
        destino = solucoes[i][0]
        soma_pesos_caminhao += distance.euclidean(origem, destino)

        for j in range(len(solucoes[i]) - 1):
            origem = solucoes[i][j]
            destino = solucoes[i][j+1]

            soma_pesos_caminhao += distance.euclidean(origem, destino)
            # soma_pesos_caminhao += math.trunc(distance.euclidean(origem, destino))
            # soma_pesos_caminhao += self.pesos[solucoes[i][j]][solucoes[i][j+1]]

        origem = solucoes[i][len(solucoes[i]) - 1]
        destino = vrp.nodes[0]
        soma_pesos_caminhao += distance.euclidean(origem, destino)

        soma_pesos_rota += math.trunc(soma_pesos_caminhao)
        
    return soma_pesos_rota

print(avaliacao(vrp, solucoes))