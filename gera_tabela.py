import sys
import os

lista_arquivos = sys.argv[1]
pasta_saida = sys.argv[2]

arquivos = []

with open(lista_arquivos, 'r') as f:
    for line in f:
        arquivos.append(line.replace('\n', ''))

tabela = ""

for arquivo in arquivos:
    with open(arquivo, 'r') as f:
        linhas = f.readlines()

        tabela += os.path.basename(arquivo) + ';' + linhas[0].replace('\n', '') + '\n'

with open(pasta_saida + '/tabelas.csv', 'w') as f:
    f.write(tabela)