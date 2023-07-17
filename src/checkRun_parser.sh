#!/bin/bash
name=parser
make clean && clear && clear && make && clear && clear && echo "[RUN - DEBUG]" && echo -e
valgrind -s --leak-check=full --track-origins=yes --show-leak-kinds=all ./$name $@