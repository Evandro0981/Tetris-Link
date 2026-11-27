'''
    tela_como_jogar.py
    Tela COMO JOGAR: mostra o tutorial do jogo em páginas, com a logo no topo.

    O texto fica em conteudo_tutorial.py. Esta classe só cuida de montar as
    páginas (quebrando as seções que não cabem) e de desenhá-las.
'''

from config.tutorial import SECOES_TUTORIAL
from config.cores import *
from os import path
import pygame

def _achar_arquivo(*partes):
    '''Procura um arquivo do jogo, mesmo que o programa seja aberto de outra pasta.'''
    candidatos = [
        path.join(*partes),
        path.join('src', *partes),
        path.join(path.dirname(__file__), *partes),
    ]
    return next((c for c in candidatos if path.exists(c)), None)


def _carregar_fonte(tamanho, padrao=False):
    caminho = None if padrao else _achar_arquivo('graficos', 'Russo_One.ttf')
    try:
        return pygame.font.Font(caminho, tamanho)
    except Exception:
        return pygame.font.Font(None, tamanho)


def _quebrar_texto(texto, fonte, largura):
    '''Quebra o texto em linhas que caibam na largura indicada.'''
    linhas = []
    for paragrafo in texto.split('\n'):
        atual = ''
        for palavra in paragrafo.split(' '):
            tentativa = palavra if not atual else atual + ' ' + palavra
            if fonte.size(tentativa)[0] <= largura or not atual:
                atual = tentativa
            else:
                linhas.append(atual)
                atual = palavra
        linhas.append(atual)
    return linhas


class TelaComoJogar:
    def __init__(self, superficie, desenhar_botao, img_logo=None):
        self.superficie = superficie
        self.desenhar_botao = desenhar_botao  # função (rect, texto, ativo) -> hover

        largura_tela = superficie.get_width()
        altura_tela = superficie.get_height()

        # Card central
        largura_card = min(1060, largura_tela - 60)
        altura_card = min(790, altura_tela - 40)
        self.rect_card = pygame.Rect(
            (largura_tela - largura_card) // 2,
            (altura_tela - altura_card) // 2,
            largura_card,
            altura_card,
        )

        # Fontes
        self.fonte_texto = _carregar_fonte(25, padrao=True)
        self.fonte_tabela = _carregar_fonte(23, padrao=True)
        self.fonte_cabecalho = _carregar_fonte(14)
        self.fonte_sub = _carregar_fonte(17)
        self.fonte_numero = _carregar_fonte(16)
        self.fonte_titulo = _carregar_fonte(24)
        self.fonte_pagina = _carregar_fonte(14)

        # Logo no topo do card
        self.logo = None
        if img_logo is not None:
            largura_logo = 300
            altura_logo = int(largura_logo * img_logo.get_height() / img_logo.get_width())
            self.logo = pygame.transform.smoothscale(img_logo, (largura_logo, altura_logo))
        altura_logo = self.logo.get_height() if self.logo else 40

        # Áreas do card
        self.y_logo = self.rect_card.y + 16
        self.y_titulo = self.y_logo + altura_logo + 22
        self.y_separador = self.y_titulo + 24
        margem = 48
        self.rect_conteudo = pygame.Rect(
            self.rect_card.x + margem,
            self.y_separador + 16,
            self.rect_card.width - 2 * margem,
            (self.rect_card.bottom - 84) - (self.y_separador + 16),
        )

        # Botões de navegação
        y_botoes = self.rect_card.bottom - 66
        largura_botao = 200
        self.rect_anterior = pygame.Rect(self.rect_card.x + margem, y_botoes, largura_botao, 46)
        self.rect_voltar = pygame.Rect(self.rect_card.centerx - largura_botao // 2, y_botoes, largura_botao, 46)
        self.rect_proxima = pygame.Rect(self.rect_card.right - margem - largura_botao, y_botoes, largura_botao, 46)

        # Imagens das peças, exibidas lado a lado na seção 1
        self.imagens_pecas = []
        for letra in 'IOTSZJL':
            caminho = _achar_arquivo('graficos', f'{letra}.png')
            if caminho:
                try:
                    img = pygame.image.load(caminho)
                    tamanho = (int(img.get_width() * 0.6), int(img.get_height() * 0.6))
                    self.imagens_pecas.append(pygame.transform.smoothscale(img, tamanho))
                except Exception:
                    pass

        self.paginas = self._montar_paginas()
        self.pagina_atual = 0

    # ------------------------------------------------------------------
    # Montagem das páginas
    # ------------------------------------------------------------------
    def _pedaco(self, altura, ops, espaco=0, manter_com_proximo=False, cabecalho=None):
        return {'altura': altura, 'ops': ops, 'espaco': espaco,
                'manter': manter_com_proximo, 'cabecalho': cabecalho}

    def _pedacos_paragrafo(self, texto):
        largura = self.rect_conteudo.width
        altura_linha = self.fonte_texto.get_linesize() + 2
        linhas = _quebrar_texto(texto, self.fonte_texto, largura)
        pedacos = []
        for i, linha in enumerate(linhas):
            surf = self.fonte_texto.render(linha, True, LINHA_COR)
            espaco = 12 if i == len(linhas) - 1 else 0
            pedacos.append(self._pedaco(altura_linha, [('img', surf, 0, 0)], espaco))
        return pedacos

    def _pedacos_subtitulo(self, texto):
        surf = self.fonte_sub.render(texto, True, DOURADO)
        return [self._pedaco(surf.get_height() + 4, [('img', surf, 0, 0)], 4, manter_com_proximo=True)]

    def _pedacos_lista(self, itens, numerada=False):
        recuo = 30
        largura = self.rect_conteudo.width - recuo
        altura_linha = self.fonte_texto.get_linesize() + 2
        pedacos = []
        for n, item in enumerate(itens, start=1):
            ops = []
            if numerada:
                marcador = self.fonte_numero.render(f'{n}.', True, DOURADO)
                ops.append(('img', marcador, 2, 1))
            else:
                meio = altura_linha // 2 - 1
                ops.append(('rect', (6, meio - 4, 8, 8), DOURADO, 1))
            linhas = _quebrar_texto(item, self.fonte_texto, largura)
            for i, linha in enumerate(linhas):
                ops.append(('img', self.fonte_texto.render(linha, True, LINHA_COR), recuo, i * altura_linha))
            pedacos.append(self._pedaco(len(linhas) * altura_linha, ops, 6))
        if pedacos:
            pedacos[-1]['espaco'] = 12
        return pedacos

    def _linha_tabela(self, celulas, larguras, fonte, cor_texto, cor_fundo, icones=None):
        '''Monta uma linha de tabela. celulas = textos; icones = {coluna: superfície}.'''
        pad_x, pad_y = 10, 7
        altura_texto = fonte.get_linesize()
        colunas = []
        altura = 0
        for c, texto in enumerate(celulas):
            icone = icones.get(c) if icones else None
            largura_util = larguras[c] - 2 * pad_x - (icone.get_width() + 10 if icone else 0)
            linhas = _quebrar_texto(texto, fonte, max(40, largura_util))
            altura_celula = max(len(linhas) * altura_texto, icone.get_height() if icone else 0)
            altura = max(altura, altura_celula + 2 * pad_y)
            colunas.append((linhas, icone))

        largura_total = sum(larguras)
        ops = []
        if cor_fundo:
            ops.append(('rect', (0, 0, largura_total, altura), cor_fundo, 0))
        ops.append(('rect', (0, altura - 1, largura_total, 1), COR_GRADE, 0))

        x = 0
        for c, (linhas, icone) in enumerate(colunas):
            x_texto = x + pad_x
            if icone:
                ops.append(('img', icone, x_texto, (altura - icone.get_height()) // 2))
                x_texto += icone.get_width() + 10
            y_texto = (altura - len(linhas) * altura_texto) // 2
            for i, linha in enumerate(linhas):
                ops.append(('img', fonte.render(linha, True, cor_texto), x_texto, y_texto + i * altura_texto))
            x += larguras[c]
        return self._pedaco(altura, ops)

    def _pedacos_tabela(self, cabecalho, linhas, fracoes, icones_por_linha=None):
        largura = self.rect_conteudo.width
        larguras = [int(f * largura) for f in fracoes]
        larguras[-1] = largura - sum(larguras[:-1])

        cab = self._linha_tabela(cabecalho, larguras, self.fonte_cabecalho, BRANCO, CINZA_HOVER)
        cab['manter'] = True
        pedacos = [cab]
        for i, linha in enumerate(linhas):
            icones = icones_por_linha[i] if icones_por_linha else None
            fundo = COR_LINHA_ALTERNADA if i % 2 else None
            pedaco = self._linha_tabela(linha, larguras, self.fonte_tabela, LINHA_COR, fundo, icones)
            pedaco['cabecalho'] = cab
            pedacos.append(pedaco)
        pedacos[-1]['espaco'] = 14
        return pedacos

    def _pedacos_bloco(self, bloco):
        tipo = bloco[0]
        if tipo == 'p':
            return self._pedacos_paragrafo(bloco[1])
        if tipo == 'sub':
            return self._pedacos_subtitulo(bloco[1])
        if tipo == 'lista':
            return self._pedacos_lista(bloco[1])
        if tipo == 'num':
            return self._pedacos_lista(bloco[1], numerada=True)
        if tipo == 'tabela':
            return self._pedacos_tabela(bloco[1], bloco[2], bloco[3])
        if tipo == 'pecas':
            return self._pedacos_pecas()
        return []

    def _pedacos_pecas(self):
        '''Imagens de todas as peças lado a lado, centralizadas e alinhadas pela base.'''
        if not self.imagens_pecas:
            return []
        espaco = 40
        largura_total = sum(img.get_width() for img in self.imagens_pecas) + espaco * (len(self.imagens_pecas) - 1)
        altura = max(img.get_height() for img in self.imagens_pecas)
        x = (self.rect_conteudo.width - largura_total) // 2
        ops = []
        for img in self.imagens_pecas:
            ops.append(('img', img, x, altura - img.get_height()))
            x += img.get_width() + espaco
        return [self._pedaco(altura, ops, 20)]

    def _montar_paginas(self):
        altura_max = self.rect_conteudo.height
        paginas = []
        for secao in SECOES_TUTORIAL:
            pedacos = []
            for bloco in secao['blocos']:
                pedacos.extend(self._pedacos_bloco(bloco))

            pagina = {'titulo': secao['titulo'], 'itens': []}
            y = 0
            for i, pedaco in enumerate(pedacos):
                necessario = pedaco['altura']
                if pedaco['manter'] and i + 1 < len(pedacos):
                    necessario += pedaco['espaco'] + pedacos[i + 1]['altura']
                if y > 0 and y + necessario > altura_max:
                    paginas.append(pagina)
                    pagina = {'titulo': secao['titulo'] + ' (cont.)', 'itens': []}
                    y = 0
                    # Tabela quebrada: repete o cabeçalho na página nova
                    if pedaco['cabecalho'] is not None:
                        pagina['itens'].append((pedaco['cabecalho'], 0))
                        y += pedaco['cabecalho']['altura']
                pagina['itens'].append((pedaco, y))
                y += pedaco['altura'] + pedaco['espaco']
            paginas.append(pagina)
        return paginas

    # ------------------------------------------------------------------
    # Eventos
    # ------------------------------------------------------------------
    def abrir(self):
        self.pagina_atual = 0

    def _mudar_pagina(self, passo):
        self.pagina_atual = max(0, min(len(self.paginas) - 1, self.pagina_atual + passo))

    def tratar_evento(self, evento):
        '''Retorna True quando a tela deve ser fechada.'''
        if evento.type == pygame.MOUSEBUTTONDOWN and evento.button == 1:
            if self.rect_voltar.collidepoint(evento.pos) or not self.rect_card.collidepoint(evento.pos):
                return True
            if self.rect_anterior.collidepoint(evento.pos):
                self._mudar_pagina(-1)
            elif self.rect_proxima.collidepoint(evento.pos):
                self._mudar_pagina(1)
        elif evento.type == pygame.MOUSEWHEEL:
            self._mudar_pagina(-1 if evento.y > 0 else 1)
        elif evento.type == pygame.KEYDOWN:
            if evento.key == pygame.K_ESCAPE:
                return True
            if evento.key in (pygame.K_RIGHT, pygame.K_PAGEDOWN, pygame.K_d):
                self._mudar_pagina(1)
            elif evento.key in (pygame.K_LEFT, pygame.K_PAGEUP, pygame.K_a):
                self._mudar_pagina(-1)
        return False

    # ------------------------------------------------------------------
    # Desenho
    # ------------------------------------------------------------------
    def desenhar(self):
        card = self.rect_card

        # Card com relevo
        relevo = pygame.Rect(card.x, card.y + 6, card.width, card.height)
        pygame.draw.rect(self.superficie, COR_RELEVO, relevo, border_radius=8)
        pygame.draw.rect(self.superficie, CINZA_BOTAO, card, border_radius=8)
        pygame.draw.rect(self.superficie, BRANCO, card, width=2, border_radius=8)

        # Logo (ou o nome do jogo, se a imagem não existir)
        if self.logo:
            self.superficie.blit(self.logo, self.logo.get_rect(midtop=(card.centerx, self.y_logo)))
        else:
            nome = self.fonte_titulo.render('TETRA-LINK', True, BRANCO)
            self.superficie.blit(nome, nome.get_rect(midtop=(card.centerx, self.y_logo)))

        # Título da página e numeração
        pagina = self.paginas[self.pagina_atual]
        titulo = self.fonte_titulo.render(pagina['titulo'], True, BRANCO)
        self.superficie.blit(titulo, titulo.get_rect(center=(card.centerx, self.y_titulo)))

        numero = self.fonte_pagina.render(f'{self.pagina_atual + 1} / {len(self.paginas)}', True, CIANO)
        self.superficie.blit(numero, numero.get_rect(topright=(card.right - 28, card.y + 22)))

        pygame.draw.line(self.superficie, COR_GRADE,
                         (self.rect_conteudo.x, self.y_separador), (self.rect_conteudo.right, self.y_separador), 2)

        # Conteúdo
        x0, y0 = self.rect_conteudo.topleft
        for pedaco, y in pagina['itens']:
            for op in pedaco['ops']:
                if op[0] == 'img':
                    _, surf, dx, dy = op
                    self.superficie.blit(surf, (x0 + dx, y0 + y + dy))
                elif op[0] == 'rect':
                    _, (dx, dy, w, h), cor, raio = op
                    pygame.draw.rect(self.superficie, cor, (x0 + dx, y0 + y + dy, w, h), border_radius=raio)

        # Botões de navegação
        tem_anterior = self.pagina_atual > 0
        tem_proxima = self.pagina_atual < len(self.paginas) - 1
        hover_anterior = self.desenhar_botao(self.rect_anterior, '< ANTERIOR', tem_anterior)
        hover_voltar = self.desenhar_botao(self.rect_voltar, 'VOLTAR')
        hover_proxima = self.desenhar_botao(self.rect_proxima, 'PRÓXIMA >', tem_proxima)

        try:
            if hover_anterior or hover_voltar or hover_proxima:
                pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_HAND)
            else:
                pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_ARROW)
        except Exception:
            pass
