#!/bin/bash

for instancia in $(cat instancias.txt)
do
    python3 genetic_algorithm.py ../instancias-solucoes/Instancias/A/$instancia.vrp 100 0.025 1000 10 ./Testes/
done