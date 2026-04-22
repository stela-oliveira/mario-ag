import os
import json
import csv
from random import random
from multiprocessing import Pool, cpu_count
from Individuo import Individuo

NUM_WORKERS = max(1, min(cpu_count() - 1, 5))


def _avaliar_individuo(cromossomo):
    os.environ['SDL_AUDIODRIVER'] = 'dummy'
    os.environ['SDL_VIDEODRIVER'] = 'dummy'
    os.environ['SDL_RENDER_DRIVER'] = 'software'
    from data import marioMain
    distance, time = marioMain.mainMario(cromossomo, redraw=False)
    return distance, time


class AlgoritmoGenetico:
    def __init__(self, tamanho_populacao, taxa_mutacao, taxa_crossover, tamanho_torneio, tamanho_elitismo):
        self.tamanho_populacao = tamanho_populacao
        self.taxa_mutacao      = taxa_mutacao
        self.taxa_crossover    = taxa_crossover
        self.tamanho_torneio   = tamanho_torneio
        self.tamanho_elitismo  = tamanho_elitismo
        self.populacao         = []
        self.geracao           = 0
        self.melhor_solucao    = None
        self.lista_solucoes    = []

    def inicializa_populacao(self):
        self.populacao = [Individuo() for _ in range(self.tamanho_populacao)]
        self.melhor_solucao = self.populacao[0]

    def avalia_populacao(self):
        cromossomos = [ind.cromossomo for ind in self.populacao]
        with Pool(processes=NUM_WORKERS) as pool:
            resultados = pool.map(_avaliar_individuo, cromossomos)
        for ind, (distance, time) in zip(self.populacao, resultados):
            ind.avaliacao(distance, time)

    def ordena_populacao(self):
        self.populacao = sorted(
            self.populacao,
            key=lambda ind: ind.nota_avaliacao,
            reverse=True
        )

    def atualiza_melhor_solucao(self):
        melhor_geracao = self.populacao[0]
        if self.melhor_solucao is None or melhor_geracao.nota_avaliacao > self.melhor_solucao.nota_avaliacao:
            self.melhor_solucao = Individuo(
                geracao=melhor_geracao.geracao,
                cromossomo=melhor_geracao.cromossomo
            )
            self.melhor_solucao.nota_avaliacao = melhor_geracao.nota_avaliacao

    def soma_avaliacoes(self):
        return sum(ind.nota_avaliacao for ind in self.populacao)

    def seleciona_pai_roleta(self, soma_avaliacao):
        if soma_avaliacao == 0:
            return 0
        valor_sorteado = random() * soma_avaliacao
        soma = 0
        for i, ind in enumerate(self.populacao):
            soma += ind.nota_avaliacao
            if soma >= valor_sorteado:
                return i
        return len(self.populacao) - 1

    def visualiza_geracao(self):
        melhor = self.populacao[0]
        media = sum(ind.nota_avaliacao for ind in self.populacao) / len(self.populacao)
        print(
            f"G:{melhor.geracao:>4} | "
            f"Melhor: {melhor.nota_avaliacao:>6} | "
            f"Media: {media:>7.1f} | "
            f"Genes: {len(melhor.cromossomo):>4} | "
            f"Melhor geral: {self.melhor_solucao.nota_avaliacao:>6}"
        )

    def resolver(self, numero_geracoes, pasta_populacao, nome_populacao):
        os.makedirs(pasta_populacao, exist_ok=True)
        arquivo_pop   = os.path.join(pasta_populacao, f'{nome_populacao}.json')
        arquivo_hist  = os.path.join(pasta_populacao, f'{nome_populacao}_historico.json')
        arquivo_best  = os.path.join(pasta_populacao, f'{nome_populacao}_best.csv')

        if os.path.isfile(arquivo_pop):
            self._carregar(arquivo_pop)
            print(f'[INFO] Populacao carregada: {len(self.populacao)} individuos. Geracao base: {self.geracao}\n')
        else:
            self.inicializa_populacao()
            print(f'[INFO] Nova populacao criada com {self.tamanho_populacao} individuos.\n')

        historico = self._carregar_historico(arquivo_hist)

        for _ in range(numero_geracoes):
            self.geracao += 1

            print(f'\n{"─"*65}')
            print(f'  GERACAO {self.geracao}')
            print(f'{"─"*65}')

            self.avalia_populacao()

            for i, ind in enumerate(self.populacao):
                ind.geracao = self.geracao
                print(
                    f'  Ind {i+1:>3}/{self.tamanho_populacao} | '
                    f'Dist: {ind.nota_avaliacao:>6} | '
                    f'Genes: {len(ind.cromossomo):>4}'
                )

            self.ordena_populacao()
            self.atualiza_melhor_solucao()
            self.visualiza_geracao()
            self.lista_solucoes.append(self.melhor_solucao.nota_avaliacao)

            historico.append({
                'geracao':        self.geracao,
                'melhor_fitness': self.populacao[0].nota_avaliacao,
                'media_fitness':  round(sum(i.nota_avaliacao for i in self.populacao) / len(self.populacao), 1),
                'melhor_geral':   self.melhor_solucao.nota_avaliacao
            })

            self._salvar(arquivo_pop)
            self._salvar_historico(arquivo_hist, historico)
            self._salvar_melhor_csv(arquivo_best)
            print(f'  [SALVO] Geracao {self.geracao} | Melhor geral: {self.melhor_solucao.nota_avaliacao}')

            if self.melhor_solucao.nota_avaliacao >= 3300:
                print(f'\n🎉 MARIO PASSOU A FASE! Fitness={self.melhor_solucao.nota_avaliacao} na geracao {self.geracao}')
                break

            self._nova_geracao()

        print(f'\n{"="*65}')
        print(f'  FIM DO TREINAMENTO')
        print(f'  Melhor fitness: {self.melhor_solucao.nota_avaliacao}')
        print(f'  Melhor encontrado na geracao: {self.melhor_solucao.geracao}')
        print(f'{"="*65}')

    def _nova_geracao(self):
        soma = self.soma_avaliacoes()
        nova_populacao = []

        for _ in range(0, self.tamanho_populacao, 2):
            pai1 = self.seleciona_pai_roleta(soma)
            pai2 = self.seleciona_pai_roleta(soma)

            if random() < self.taxa_crossover:
                filhos = self.populacao[pai1].crossover(self.populacao[pai2])
            else:
                filhos = [
                    Individuo(geracao=self.geracao, cromossomo=self.populacao[pai1].cromossomo),
                    Individuo(geracao=self.geracao, cromossomo=self.populacao[pai2].cromossomo)
                ]

            nova_populacao.append(filhos[0].mutacao(self.taxa_mutacao))
            nova_populacao.append(filhos[1].mutacao(self.taxa_mutacao))

        nova_populacao = nova_populacao[:self.tamanho_populacao]

        # Elitismo: garante que os melhores da geracao anterior ficam nos primeiros indices
        for i in range(self.tamanho_elitismo):
            nova_populacao[i] = Individuo(
                geracao=self.populacao[i].geracao,
                cromossomo=self.populacao[i].cromossomo
            )
            nova_populacao[i].nota_avaliacao = self.populacao[i].nota_avaliacao

        self.populacao = nova_populacao

    def _salvar(self, arquivo):
        # populacao ordenada: indice 0 = sempre o melhor
        dados = {
            'geracao':   self.geracao,
            'populacao': [ind.to_dict() for ind in self.populacao]
        }
        with open(arquivo, 'w', encoding='utf-8') as f:
            json.dump(dados, f, indent=2)

    def _carregar(self, arquivo):
        with open(arquivo, 'r', encoding='utf-8') as f:
            dados = json.load(f)
        self.geracao   = dados.get('geracao', 0)
        self.populacao = [Individuo.from_dict(d) for d in dados['populacao']]
        self.ordena_populacao()
        self.melhor_solucao = Individuo(
            geracao=self.populacao[0].geracao,
            cromossomo=self.populacao[0].cromossomo
        )
        self.melhor_solucao.nota_avaliacao = self.populacao[0].nota_avaliacao

    def _salvar_historico(self, arquivo, historico):
        with open(arquivo, 'w', encoding='utf-8') as f:
            json.dump(historico, f, indent=2)

    def _carregar_historico(self, arquivo):
        if os.path.isfile(arquivo):
            with open(arquivo, 'r', encoding='utf-8') as f:
                return json.load(f)
        return []

    def _salvar_melhor_csv(self, arquivo):
        with open(arquivo, 'w', newline='') as f:
            writer = csv.writer(f, delimiter=';')
            writer.writerow(self.melhor_solucao.cromossomo)
