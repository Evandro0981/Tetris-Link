'''
    conteudo_tutorial.py
    Texto do tutorial exibido na tela COMO JOGAR.

    Cada seção vira uma ou mais páginas (a tela quebra a seção sozinha se o
    conteúdo não couber). Tipos de bloco:
        ('p', texto)                 parágrafo
        ('sub', texto)               subtítulo
        ('lista', [itens])           lista com marcadores
        ('num', [itens])             lista numerada
        ('tabela', cabecalho, linhas, larguras)
                                     larguras = frações da largura total
        ('pecas',)                   imagens das sete peças, lado a lado
'''

SECOES_TUTORIAL = [
    {
        'titulo': '1. Regras básicas',
        'blocos': [
            ('p', 'Objetivo: encaixar as peças que caem para formar linhas horizontais completas. '
                  'O tabuleiro tem 10 colunas por 20 linhas. Uma linha totalmente preenchida '
                  'desaparece, os blocos de cima descem e a equipe ganha pontos.'),
            ('p', 'As peças são sete, todas com quatro blocos, e chegam em ordem aleatória:'),
            ('pecas',),
            ('sub', 'Como uma peça se comporta'),
            ('num', [
                'Ela surge no alto, no meio do tabuleiro, e desce sozinha uma linha por vez.',
                'Enquanto desce, você pode movê-la para os lados, girá-la e acelerar a queda.',
                'Quando encosta no fundo ou em outro bloco, ela trava no lugar e a próxima peça aparece.',
            ]),
        ],
    },
    {
        'titulo': '2. A tela de partida',
        'blocos': [
            ('p', 'A janela sempre mostra dois tabuleiros lado a lado: Equipe 1 à esquerda e '
                  'Equipe 2 à direita.'),
            ('p', 'No topo de cada tabuleiro aparece o nome da equipe. No modo em rede, sua equipe '
                  'aparece como EQUIPE X (SUA) em azul-claro e a outra como (ADVERSÁRIA) em vermelho.'),
            ('p', 'Na margem de baixo da janela aparece uma linha amarela:'),
            ('lista', [
                'no modo local: "MODO LOCAL | Equipe 1: WASD - Equipe 2: Setas";',
                'no modo em rede: a sua função, por exemplo "SUA FUNÇÃO: ROTAÇÃO DA EQUIPE 2".',
            ]),
        ],
    },
    {
        'titulo': '3. Modo 1 versus 1 (mesmo computador)',
        'blocos': [
            ('p', 'O modo local roda num só computador, sem servidor e sem rede. Para começar, '
                  'clique em 1 VERSUS 1 na tela inicial, sem se conectar a um servidor. As peças '
                  'começam a cair nos dois tabuleiros ao mesmo tempo.'),
            ('sub', 'Dois jogadores, no mesmo teclado'),
            ('lista', [
                'Jogador 1 fica com o tabuleiro da esquerda e as teclas W A S D.',
                'Jogador 2 fica com o tabuleiro da direita e as setas.',
                'Cada um move e gira as próprias peças. Os tabuleiros são independentes: as linhas '
                'que um completa não afetam o outro.',
                'Quem acaba primeiro fica olhando o outro jogar. Quando os dois tabuleiros terminam, '
                'a tela final mostra quem fez mais pontos.',
            ]),
            ('sub', 'Jogando sozinho'),
            ('lista', [
                'O jogo sempre abre os dois tabuleiros. Escolha um lado: o da esquerda usa W A S D; '
                'o da direita usa as setas.',
                'O tabuleiro que ninguém controla continua recebendo peças, enche logo e mostra '
                'FIM DE JOGO; o seu segue normalmente.',
                'A partida termina quando o seu tabuleiro também encher. O desafio é bater o seu '
                'próprio recorde de pontos.',
            ]),
            ('p', 'Apertar Esc durante a partida abandona o jogo e volta à tela inicial.'),
        ],
    },
    {
        'titulo': '4. Modo 2 versus 2 (em rede)',
        'blocos': [
            ('p', 'Jogam exatamente 4 pessoas, cada uma no seu computador, divididas em duas duplas. '
                  'Dentro de cada dupla, um jogador só move a peça e o outro só gira. '
                  'Vence a dupla que fizer mais pontos.'),
            ('sub', 'Preparando a partida'),
            ('num', [
                'Escolha um computador para deixar o servidor do jogo rodando (servidor.py, na pasta src).',
                'Todos os jogadores devem estar na mesma rede desse computador.',
                'Na tela inicial, cada jogador digita o IP do servidor (ex: 10.3.1.17) e clica em 2 VERSUS 2.',
                'A partida começa sozinha assim que o quarto jogador se conecta.',
            ]),
            ('sub', 'Como as duplas são formadas'),
            ('tabela', ['Ordem em que conectou', 'Equipe', 'Tabuleiro'], [
                ['1º e 2º jogadores', 'Equipe 1', 'esquerda'],
                ['3º e 4º jogadores', 'Equipe 2', 'direita'],
            ], [0.5, 0.25, 0.25]),
            ('p', 'Dentro de cada dupla, o servidor sorteia quem fica com cada função. Para escolher '
                  'as duplas, conectem-se na ordem combinada: primeiro os dois da Equipe 1, depois '
                  'os dois da Equipe 2.'),
            ('sub', 'As duas funções'),
            ('tabela', ['Função', 'O que faz'], [
                ['MOVIMENTO', 'A e D (ou as setas para os lados) movem a peça para os lados; '
                              'S (ou a seta para baixo) faz a peça cair mais rápido.'],
                ['ROTAÇÃO', 'W (ou a seta para cima) gira a peça.'],
            ], [0.25, 0.75]),
        ],
    },
    {
        'titulo': '5. Controles',
        'blocos': [
            ('tabela', ['Ação', 'Tabuleiro esquerdo', 'Tabuleiro direito'], [
                ['Mover para a esquerda', 'A', 'Seta esquerda'],
                ['Mover para a direita', 'D', 'Seta direita'],
                ['Girar a peça', 'W', 'Seta para cima'],
                ['Cair mais rápido (segurar)', 'S', 'Seta para baixo'],
                ['Abandonar a partida', 'Esc', 'Esc'],
            ], [0.4, 0.3, 0.3]),
            ('sub', 'Detalhes que fazem diferença'),
            ('lista', [
                'Segurar uma seta lateral move a peça de casa em casa, com uma pequena pausa entre '
                'cada passo. Para a rotação, a pausa entre giros é um pouco maior.',
                'Para baixo acelera a queda enquanto a tecla está pressionada; não existe queda instantânea.',
                'Cada giro vira a peça 90 graus. O quadrado amarelo (peça O) não gira.',
                'O giro não empurra a peça: se ela for sair do tabuleiro ou bater em outro bloco, '
                'simplesmente não gira. Encostada na parede, afaste-a uma casa antes de girar.',
            ]),
        ],
    },
    {
        'titulo': '6. Dicas para fazer mais pontos',
        'blocos': [
            ('lista', [
                'Mantenha a superfície da pilha o mais plana possível e evite deixar buracos cobertos.',
                'Deixe uma coluna livre na lateral e guarde-a para a peça reta (I, azul-clara): quatro '
                'linhas de uma vez valem 1200 x level, trinta vezes mais que uma linha sozinha.',
                'Olhe a prévia antes de posicionar a peça atual, para já deixar espaço para a próxima.',
                'Acelere a queda só quando a peça já estiver na coluna e na posição certas.',
            ]),
        ],
    },
]
