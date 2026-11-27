import pygame
from config.cores import *

# Tamanho da janela do jogo
COLUNAS = 10
LINHAS = 20
TAMANHO_CELULA = 40

LARGURA_JOGO = COLUNAS * TAMANHO_CELULA  # 400px
ALTURA_JOGO = LINHAS * TAMANHO_CELULA   # 800px

# Barra lateral.
LARGURA_BARRA_LATERAL = 200
FRACAO_ALTURA_PREVIA = 0.7
FRACAO_ALTURA_PONTUACAO = 1 - FRACAO_ALTURA_PREVIA

# Janela-Agrupamento (Dois Tabuleiros)
ESPACAMENTO = 20

# Tamanhos de fontes do game
TAMANHO_FONTE_CONTAGEM = 96
TAMANHO_FONTE_INFORMACOES = 16
TAMANHO_FONTE_FIM_JOGO = 48

# Caminho do icone do game.
PATH_ICON_GAME = "img/icon.png"

TEMPO_ESPERA_REVANCHE = 3000  # ms — tempo para outros jogadores clicarem
TEMPO_ESPERA_INICIO_JOGO = 5000

# Largura de 1 conjunto completo (Jogo + Barra Lateral + Espaço)
LARGURA_TABULEIRO_COMPLETO = LARGURA_JOGO + LARGURA_BARRA_LATERAL + ESPACAMENTO

# Largura total para os 2 tabuleiros lado a lado
LARGURA_JANELA = (LARGURA_TABULEIRO_COMPLETO * 2) + (ESPACAMENTO * 2)
ALTURA_JANELA = ALTURA_JOGO + ESPACAMENTO * 2

# Comportamento do jogo
VELOCIDADE_ATUALIZACAO_INICIAL = 400
VELOCIDADE_DESCIDA_PECA = 0.3
TEMPO_ESPERA_MOVER = 150
TEMPO_ESPERA_ROTACIONAR = 200
DESLOCAMENTO_BLOCO = pygame.Vector2(COLUNAS // 2, -1)

OFFSET_EQ1 = 0
OFFSET_EQ2 = LARGURA_TABULEIRO_COMPLETO + ESPACAMENTO
NOMES_FUNCAO = {'MOVIMENTO': 'MOVIMENTO', 'ROTACAO': 'ROTAÇÃO'}

CENTRO_JOGO_EQ1 = (ESPACAMENTO + OFFSET_EQ1 + LARGURA_JOGO // 2, ESPACAMENTO + ALTURA_JOGO // 2)
CENTRO_JOGO_EQ2 = (ESPACAMENTO + OFFSET_EQ2 + LARGURA_JOGO // 2, ESPACAMENTO + ALTURA_JOGO // 2)

# Formas do tetris
TETROMINOS = {
     'T': {'forma': [(0,0), (-1,0), (1,0), (0,-1)], 'cor': ROXO},
     'O': {'forma': [(0,0), (0,-1), (1,0), (1,-1)], 'cor': AMARELO},
     'J': {'forma': [(0,0), (0,-1), (0,1), (-1,1)], 'cor': AZUL},
     'L': {'forma': [(0,0), (0,-1), (0,1), (1,1)], 'cor': LARANJA},
     'I': {'forma': [(0,0), (0,-1), (0,-2), (0,1)], 'cor': CIANO},
     'S': {'forma': [(0,0), (-1,0), (0,-1), (1,-1)], 'cor': VERDE},
     'Z': {'forma': [(0,0), (1,0), (0,-1), (-1,-1)], 'cor': VERMELHO},
}

PONTOS_DADOS = {1: 40, 2: 100, 3: 300, 4: 1200}

# Defini o total de peças geradas aleatoriamente
TOTAL_PECAS_SORTEADAS = 5

# Textos de informações do jogo
TEXTO_FUNCAO_EQUIPES_OFFLINE = "Equipe 1 (WASD)    |    MODO LOCAL    |    Equipe 2 (→ ↑ ← ↓)"

# Configurações do servidor multiplayer
MAX_JOGADORES_MULTIPLAYER = 4
MAX_BUFFER_MENSAGEM = 8192
CODIFICACAO = "utf-8"
HOST = '0.0.0.0'
PORT = 5555