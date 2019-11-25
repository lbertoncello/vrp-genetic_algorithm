#!/bin/bash

echo "python3 genetic_algorithm.py ../instancias-solucoes/Instancias/A/A-n32-k5.vrp 100 0.75 1000 10"
python3 genetic_algorithm.py ../instancias-solucoes/Instancias/A/A-n32-k5.vrp 100 0.75 1000 3

echo "python3 genetic_algorithm.py ../instancias-solucoes/Instancias/A/A-n32-k5.vrp 100 0.01 2000 10"
python3 genetic_algorithm.py ../instancias-solucoes/Instancias/A/A-n32-k5.vrp 100 0.10 1000 3

echo "python3 genetic_algorithm.py ../instancias-solucoes/Instancias/A/A-n32-k5.vrp 100 0.15 1000 10"
python3 genetic_algorithm.py ../instancias-solucoes/Instancias/A/A-n32-k5.vrp 100 0.15 1000 3

echo "python3 genetic_algorithm.py ../instancias-solucoes/Instancias/A/A-n32-k5.vrp 50 0.0001 5000 10"
python3 genetic_algorithm.py ../instancias-solucoes/Instancias/A/A-n32-k5.vrp 50 0.0001 5000 3
