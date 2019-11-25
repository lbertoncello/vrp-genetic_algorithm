#!/bin/bash


echo "python3 genetic_algorithm.py ../instancias-solucoes/Instancias/A/A-n32-k5.vrp 50 0.025 2000 10"
python3 genetic_algorithm.py ../instancias-solucoes/Instancias/A/A-n32-k5.vrp 50 0.025 2000 3

echo "python3 genetic_algorithm.py ../instancias-solucoes/Instancias/A/A-n32-k5.vrp 100 0.035 1000 10"
python3 genetic_algorithm.py ../instancias-solucoes/Instancias/A/A-n32-k5.vrp 100 0.035 1000 3

echo "python3 genetic_algorithm.py ../instancias-solucoes/Instancias/A/A-n32-k5.vrp 100 0.025 1000 10"
python3 genetic_algorithm.py ../instancias-solucoes/Instancias/A/A-n32-k5.vrp 100 0.025 1000 3 #melhor media: 857 

echo "python3 genetic_algorithm.py ../instancias-solucoes/Instancias/A/A-n32-k5.vrp 100 0.05 1000 10"
python3 genetic_algorithm.py ../instancias-solucoes/Instancias/A/A-n32-k5.vrp 100 0.05 1000 3
