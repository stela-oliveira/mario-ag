Fluxo Completo do LGP Super Mario

Estrutura do Cromossomo

    1 chromosome = [comando1, tempo1, comando2, tempo2, comando3, tempo3, ...]

Mapeamento de comandos (N_COMMANDS = 6):

| Código | Ação |
|---|---|
| 1 | action (correr / atirar) |
| 2 | jump (pular) |
| 3 | left (esquerda) |
| 4 | right (direita) |
| 5 | down (abaixar) |
| 6 | still (parado) |


Exemplo: [4, 500, 2, 300, 6, 200] =
→ Direita por 500ms → Pular por 300ms → Parado por 200ms

---

Inicialização da População

    1 # POPULATION_SIZE = 10 indivíduos
    2 # Cada cromossomo tem 20-50 instruções (comando + tempo)

    - Gera 10 cromossomos aleatórios
    - Cada gene par = comando (1-6)
    - Cada gene ímpar = duração em ms (100-1000)

---

Avaliação (TESTAR NO JOGO)

    1 for i, chromosome in enumerate(population):
    2     distance, time = decode_chromosome(chromosome)  # ← RODA O JOGO!
    3     fitness = get_fitness(distance, time)           # ← FITNESS = DISTÂNCIA

Cada indivíduo é testado rodando o jogo inteiro! O Mario segue o cromossomo automaticamente:

    1 # Em tools.py - event_loop():
    2 self.keys = chromosome[self.current_action_idx]  # comando
    3 # espera chromosome[current_action_idx+1] milissegundos
    4 # depois muda para o próximo comando

Fitness = distância percorrida (quanto mais longe, melhor)

---

Seleção por Torneio

    1 # P_TOUR = 0.7 (70% chance do melhor vencer)
    2 # TOURNAMENT_SIZE = 2

    1. Sorteia 2 indivíduos aleatórios
    2. 70% de chance: escolhe o com melhor fitness
    3. 30% de chance: escolhe o outro

---

Crossover (Recombinação)

    1 # P_CROSSOVER = 0.5 (50% de chance)

Como funciona:

    1 Pai 1: [A1, A2, A3 | B1, B2 | C1, C2, C3]
    2 Pai 2: [D1, D2 | E1, E2, E3 | F1, F2]
    3 
    4 Filho 1: [A1, A2, A3] + [E1, E2, E3] + [C1, C2, C3]
    5 Filho 2: [D1, D2] + [B1, B2] + [F1, F2]

Corta os cromossomos em 2 pontos e troca os segmentos do meio.

---

Mutação

    1 # P_MUTATE = 0.01 (1% de chance por gene)

Para cada gene:
    - 1% de chance de mutar
    - Se for comando (índice par): troca por 1-6 aleatório
    - Se for tempo (índice ímpar): troca por 100-1000ms aleatório

---

Elitismo

    1 # ELITISM_SIZE = 1

O melhor indivíduo da geração atual é copiado diretamente para a próxima (sem mudanças).

---

Fluxo Completo

    1 ┌─────────────────────────────────────────┐
    2 │ GERAÇÃO 0                               │
    3 │ ├─ Inicializa 10 cromossomos aleatórios │
    4 │ └─ Avalia cada um:                      │
    5 │    └─ RODA O JOGO COM CADA UM!          │
    6 │       └─ fitness = distância            │
    7 └─────────────────────────────────────────┘
    8          ↓
    9 ┌──────────────────────────────────────────┐
    10 │ SELEÇÃO + CROSSOVER + MUTAÇÃO           │
    11 │ ├─ Torneio para escolher pais           │
    12 │ ├─ 50% chance de crossover              │
    13 │ ├─ 1% chance de mutação por gene        │
    14 │ └─ Elitismo: melhor é preservado        │
    15 └─────────────────────────────────────────┘
    16          ↓
    17 ┌─────────────────────────────────────────┐
    18 │ GERAÇÃO 1, 2, 3, ... até 10000          │
    19 │ └─ Repete avaliação e evolução          │
    20 │    └─ SALVA POPULAÇÃO A CADA 1 GERAÇÃO  │
    21 └─────────────────────────────────────────┘

---

⚠️ Problema Atual

O código testa no jogo real a cada avaliação. Isso significa:
    - 10 indivíduos × 10000 gerações = 100.000 execuções do jogo
    - Cada execução pode levar segundos
    - Com DRAW_FRAMES = True, é muito lento
    - Com DRAW_FRAMES = False, é mais rápido mas ainda pesado