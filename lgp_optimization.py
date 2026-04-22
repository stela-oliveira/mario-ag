import sys
import pygame as pg
from AlgoritmoGenetico import AlgoritmoGenetico

TAMANHO_POPULACAO = 50
TAXA_MUTACAO      = 0.03
TAXA_CROSSOVER    = 0.80
TAMANHO_TORNEIO   = 3
TAMANHO_ELITISMO  = 2
NUMERO_GERACOES   = 300
PASTA_POPULACAO   = 'populations'

if __name__ == '__main__':
    print('=' * 65)
    print('  ALGORITMO GENETICO - SUPER MARIO BROS (Nivel 1)')
    print('=' * 65)
    print(f'  Populacao: {TAMANHO_POPULACAO} | Geracoes: {NUMERO_GERACOES}')
    print(f'  Crossover: {TAXA_CROSSOVER*100:.0f}% | Mutacao: {TAXA_MUTACAO*100:.0f}% por gene')
    print(f'  Elitismo: {TAMANHO_ELITISMO}')
    print('=' * 65)
    print('Nome da populacao (novo = cria; existente = continua):')
    nome = input().strip()

    ag = AlgoritmoGenetico(
        tamanho_populacao = TAMANHO_POPULACAO,
        taxa_mutacao      = TAXA_MUTACAO,
        taxa_crossover    = TAXA_CROSSOVER,
        tamanho_torneio   = TAMANHO_TORNEIO,
        tamanho_elitismo  = TAMANHO_ELITISMO
    )

    ag.resolver(NUMERO_GERACOES, PASTA_POPULACAO, nome)

    pg.quit()
    sys.exit()
