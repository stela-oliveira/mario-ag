import sys
import json
import os
import csv
import pygame as pg

PASTA_POPULACAO = 'populations'


def carregar_populacao(nome):
    arquivo = os.path.join(PASTA_POPULACAO, f'{nome}.json')
    if not os.path.isfile(arquivo):
        print(f'[ERRO] Arquivo {arquivo} nao encontrado.')
        sys.exit(1)
    with open(arquivo, 'r', encoding='utf-8') as f:
        dados = json.load(f)
    populacao = dados['populacao']
    geracao   = dados['geracao']
    return populacao, geracao


def carregar_melhor(nome):
    arquivo = os.path.join(PASTA_POPULACAO, f'{nome}_best.csv')
    if not os.path.isfile(arquivo):
        return None
    with open(arquivo, 'r') as f:
        reader = csv.reader(f, delimiter=';')
        for row in reader:
            return list(map(int, row))
    return None


def main():
    nome = sys.argv[1] if len(sys.argv) > 1 else input('Nome da populacao: ').strip()

    populacao, geracao = carregar_populacao(nome)

    print(f'\nPopulacao: {len(populacao)} individuos | Geracao salva: {geracao}')
    print(f'Indice 0 = MELHOR individuo (fitness: {populacao[0]["nota_avaliacao"]})')
    print(f'\nOpcoes:')
    print(f'  [0-{len(populacao)-1}] = assistir individuo pelo indice')
    print(f'  [b] = assistir o MELHOR de todos os tempos (_best.csv)')
    print(f'  [h] = ver historico de geracoes')

    escolha = input('\nEscolha: ').strip().lower()

    if escolha == 'h':
        arquivo_hist = os.path.join(PASTA_POPULACAO, f'{nome}_historico.json')
        if os.path.isfile(arquivo_hist):
            with open(arquivo_hist, 'r', encoding='utf-8') as f:
                historico = json.load(f)
            print(f'\n{"─"*55}')
            print(f'  {"Geracao":>8} | {"Melhor":>8} | {"Media":>8} | {"Melhor Geral":>12}')
            print(f'{"─"*55}')
            for h in historico:
                print(f'  {h["geracao"]:>8} | {h["melhor_fitness"]:>8} | {h["media_fitness"]:>8} | {h["melhor_geral"]:>12}')
            print(f'{"─"*55}')
        else:
            print('[INFO] Historico nao encontrado.')
        return

    if escolha == 'b':
        cromossomo = carregar_melhor(nome)
        if cromossomo is None:
            print('[ERRO] Arquivo _best.csv nao encontrado.')
            return
        print(f'\nAssistindo MELHOR individuo de todos os tempos')
    else:
        idx = int(escolha)
        if idx < 0 or idx >= len(populacao):
            print(f'[ERRO] Indice invalido. Use 0 a {len(populacao)-1}')
            return
        cromossomo = populacao[idx]['cromossomo']
        print(f'\nAssistindo individuo {idx} | Fitness salvo: {populacao[idx]["nota_avaliacao"]} | Geracao: {populacao[idx]["geracao"]}')

    print(f'Genes: {len(cromossomo)} ({len(cromossomo)//2} comandos)')
    print(f'Primeiros genes: {cromossomo[:8]}\n')

    from data import marioMain
    distance, time = marioMain.mainMario(cromossomo, redraw=True)

    print(f'\nDistancia percorrida: {distance}')
    print(f'Tempo: {time}ms')

    pg.quit()
    sys.exit()


if __name__ == '__main__':
    main()
