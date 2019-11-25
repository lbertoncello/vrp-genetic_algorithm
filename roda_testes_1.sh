#!/bin/bash

echo "python3 genetic_algorithm.py ../instancias-solucoes/Instancias/A/A-n32-k5.vrp 100 0.01 2000 10"
python3 genetic_algorithm.py ../instancias-solucoes/Instancias/A/A-n32-k5.vrp 100 0.01 2000 3

echo "python3 genetic_algorithm.py ../instancias-solucoes/Instancias/A/A-n32-k5.vrp 30 0.01 10000 10"
python3 genetic_algorithm.py ../instancias-solucoes/Instancias/A/A-n32-k5.vrp 30 0.01 10000 3

echo "python3 genetic_algorithm.py ../instancias-solucoes/Instancias/A/A-n32-k5.vrp 20 0.05 10000 10"
python3 genetic_algorithm.py ../instancias-solucoes/Instancias/A/A-n32-k5.vrp 20 0.05 10000 3

echo "python3 genetic_algorithm.py ../instancias-solucoes/Instancias/A/A-n32-k5.vrp 200 0.01 10"
python3 genetic_algorithm.py ../instancias-solucoes/Instancias/A/A-n32-k5.vrp 200 0.01 3

echo "python3 genetic_algorithm.py ../instancias-solucoes/Instancias/A/A-n32-k5.vrp 500 0.01 200 10"
python3 genetic_algorithm.py ../instancias-solucoes/Instancias/A/A-n32-k5.vrp 500 0.01 200 3

