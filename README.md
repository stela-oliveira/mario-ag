Super Mario Bros Level 1! 🍄
=============

Solução com Algoritmo Genético para o Mario passar automaticamente o Level 1.

![screenshot](https://raw.github.com/justinmeister/Mario-Level-1/master/screenshot.png)

Uma abordagem baseada em Algoritmos Genéticos (programação genética linear) para aprender o primeiro nível do simulador de IA do Mario.
Cada instrução é codificada em um cromossomo e, após cada geração, é alterada pela aplicação de cruzamentos e mutações.


DEPENDENCIES:

| Item | Versão |
|---|---|
| Python | **3.11.x** (não use 3.12+, pygame não suporta) |
| pygame | 2.x (instalado via pip) |
| numpy | 1.x (instalado via pip) |
| Docker Desktop | 29.x (só se quiser usar Docker) |

## Development Environment

Este projeto suporta desenvolvimento via Docker com suporte gráfico para o pygame e diretamente com o Python.

### Docker
---

### Após entrar na pasta do projeto, contrua a imagem (só na primeira vez)

```powershell
docker compose build
# Aguarde — pode demorar 2-5 minutos na primeira vez
```
### Iniciar o container

```powershell
docker compose up -d mario-ga
```
### Entrar no container e treinar

```powershell
docker compose exec mario-ga bash
```
Dentro do container:

```bash
python lgp_optimization.py
# Digite o nome o nome da sua população
```

> A pasta `populations/` é montada como volume — os arquivos ficam salvos no seu PC mesmo após fechar o container.

---

### Python Direto
---
### Instalar dependências

```powershell
py -3.11 -m pip install pygame numpy
```

### Entrar na pasta do projeto

```powershell
cd caminho_da_pasta/mario-ag
```
### Treinar (Terminal 1)

```powershell
$env:SDL_AUDIODRIVER = "dummy"
$env:SDL_VIDEODRIVER = "dummy"
py -3.11 lgp_optimization.py
# Quando pedir o nome da população, digite um nome e pressione Enter
```
> O treino salva automaticamente a cada geração em `populations/mario1.json`. Se fechar e abrir novamente com o **mesmo nome**, continua de onde parou.

### Assistir o Mario jogar (Terminal 2)

Abra um **segundo PowerShell** sem fechar o treino:

```powershell
$env:SDL_VIDEODRIVER = "windows"
$env:SDL_AUDIODRIVER = "dummy"
py -3.11 watch_mario.py nome_da_sua_população
```
### Aparece um menu com as opções:
```
[0-49]  → assistir indivíduo pelo índice  (0 = sempre o MELHOR)
[b]     → assistir o MELHOR de todos os tempos  (_best.csv)
[h]     → ver tabela completa do histórico de gerações
```
> O índice **0 é SEMPRE o melhor** — a população é ordenada antes de salvar.
---
## Como treinar e assistir — Linux / macOS

```bash
# Instalar dependências
pip3.11 install pygame numpy

# Treinar
SDL_AUDIODRIVER=dummy SDL_VIDEODRIVER=dummy py -3.11 lgp_optimization.py

# Assistir (Linux com X11)
SDL_VIDEODRIVER=x11 SDL_AUDIODRIVER=dummy py -3.11 watch_mario.py nome_da_população

# Assistir (macOS)
py -3.11 watch_mario.py nome_da_opulação
