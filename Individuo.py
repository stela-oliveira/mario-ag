from random import randint, random


MIN_INSTRUCTIONS = 50
MAX_INSTRUCTIONS = 400
MIN_TIME         = 50
MAX_TIME         = 300
N_COMMANDS       = 6


class Individuo:
    def __init__(self, geracao=0, cromossomo=None):
        self.geracao        = geracao
        self.nota_avaliacao = 0

        if cromossomo is not None:
            self.cromossomo = list(cromossomo)
        else:
            n = randint(MIN_INSTRUCTIONS, MAX_INSTRUCTIONS)
            self.cromossomo = []
            for _ in range(n):
                self.cromossomo.append(randint(1, N_COMMANDS))
                self.cromossomo.append(randint(MIN_TIME, MAX_TIME))

    def avaliacao(self, distance, time):
        self.nota_avaliacao = distance

    def crossover(self, outro_individuo):
        len1 = max(2, len(self.cromossomo) // 2)
        len2 = max(2, len(outro_individuo.cromossomo) // 2)
        corte1 = randint(1, len1 - 1) * 2
        corte2 = randint(1, len2 - 1) * 2

        filho1 = Individuo(geracao=self.geracao + 1)
        filho2 = Individuo(geracao=self.geracao + 1)
        filho1.cromossomo = self.cromossomo[:corte1] + outro_individuo.cromossomo[corte2:]
        filho2.cromossomo = outro_individuo.cromossomo[:corte2] + self.cromossomo[corte1:]
        return [filho1, filho2]

    def mutacao(self, taxa_mutacao):
        for i in range(len(self.cromossomo)):
            if random() < taxa_mutacao:
                if i % 2 == 0:
                    self.cromossomo[i] = randint(1, N_COMMANDS)
                else:
                    self.cromossomo[i] = randint(MIN_TIME, MAX_TIME)
        return self

    def to_dict(self):
        return {
            'geracao':        self.geracao,
            'nota_avaliacao': self.nota_avaliacao,
            'cromossomo':     self.cromossomo
        }

    @staticmethod
    def from_dict(data):
        ind = Individuo(
            geracao=data['geracao'],
            cromossomo=data['cromossomo']
        )
        ind.nota_avaliacao = data['nota_avaliacao']
        return ind
