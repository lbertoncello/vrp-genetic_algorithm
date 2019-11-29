#!/bin/bash

for instancia in $(cat instancias_5.txt)
do
    if [ "${instancia:0:1}" == "A" ]
    then
        dir="A"
    else 
        if [ "${instancia:0:1}" == "B" ]
        then
            dir="B"
        else
            if [ "${instancia:0:1}" == "F" ]
            then
                dir="F"
            fi
        fi
    fi

    python3 genetic_algorithm.py ../instancias-solucoes/Instancias/$dir/$instancia.vrp 100 0.025 1000 10 ./Testes/
done