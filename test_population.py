#!/usr/bin/env python
"""Script para testar um indivíduo de uma população salva"""

import csv
import sys
import pygame as pg
from data import marioMain

POPULATION_FOLDER = 'populations'

def load_population(population_name):
    file_path = f"{POPULATION_FOLDER}/{population_name}.txt"
    population = []
    with open(file_path, 'r') as csv_file:
        reader = csv.reader(csv_file, delimiter=';')
        for row in reader:
            population.append(list(map(int, row)))
    return population

def test_individual(chromosome, individual_idx=0):
    """Testa um indivíduo e mostra o Mario jogando"""
    print(f"Testando indivíduo {individual_idx}")
    print(f"Chromosome length: {len(chromosome)}")
    print(f"Commands: {chromosome[:10]}...")
    
    distance, time = marioMain.mainMario(chromosome, redraw=True)
    
    print(f"Distância: {distance}")
    print(f"Tempo: {time}")
    return distance, time

def main():
    if len(sys.argv) > 1:
        population_name = sys.argv[1]
    else:
        print("Nome da população:", end=" ")
        population_name = input().strip()
    
    print(f"Carregando população: {population_name}")
    population = load_population(population_name)
    print(f"População carregada com {len(population)} indivíduos")
    
    if len(sys.argv) > 2:
        individual_idx = int(sys.argv[2])
    else:
        print(f"Qual indivíduo testar? (0-{len(population)-1}):", end=" ")
        individual_idx = int(input().strip())
    
    chromosome = population[individual_idx]
    test_individual(chromosome, individual_idx)
    
    pg.quit()
    sys.exit()

if __name__ == "__main__":
    main()
