#!/usr/bin/env python3
import tkinter as tk  # Biblioteca para interface gráfica
from tkinter import messagebox  # Para mostrar caixas de mensagem (alertas)
from math import sqrt  # Para cálculos matemáticos (como altura do hexágono)
import time  # Para medir o tempo de execução das jogadas da IA

# -------------------------------------------------------
# Constantes de identificação dos jogadores
# -------------------------------------------------------
VAZIO = '-'      # Célula vazia
AZUL = 'IA'      # Jogador azul → a IA
VERMELHO = 'Humano'  # Jogador vermelho → humano

# -------------------------------------------------------
# Classe que representa o tabuleiro do jogo Hex
# -------------------------------------------------------
class TabuleiroHex:
    def __init__(self, n=5):
        self.n = n  # Tamanho do tabuleiro (n x n)
        self.grade = [[VAZIO] * n for _ in range(n)]  # Cria matriz n x n preenchida com '-'
        self.movimentos_jogados = 0  # Contador de movimentos feitos

    def copiar(self):
        # Cria uma cópia do tabuleiro (útil para simulações)
        copia = TabuleiroHex(self.n)
        copia.grade = [linha[:] for linha in self.grade]  # Copia linha por linha
        copia.movimentos_jogados = self.movimentos_jogados
        return copia

    def dentro_limite(self, r, c):
        # Verifica se a posição (r,c) está dentro do tabuleiro
        return 0 <= r < self.n and 0 <= c < self.n

    def vizinhos(self, r, c):
        # Retorna as posições vizinhas de uma célula (hexagonal → 6 vizinhos)
        direcoes = [(-1,0), (-1,1), (0,-1), (0,1), (1,-1), (1,0)]
        for dr, dc in direcoes:
            rr, cc = r + dr, c + dc  # Calcula posição vizinha
            if self.dentro_limite(rr, cc):  # Só retorna se estiver dentro do tabuleiro
                yield rr, cc

    def jogadas_possiveis(self):
        # Retorna todas as posições vazias do tabuleiro
        return [(r, c) for r in range(self.n) for c in range(self.n) if self.grade[r][c] == VAZIO]

    def jogar(self, r, c, jogador):
        # Realiza uma jogada na posição (r,c) para o jogador
        if not self.dentro_limite(r, c) or self.grade[r][c] != VAZIO:
            return False  # Se inválido ou ocupado, retorna False
        self.grade[r][c] = jogador
        self.movimentos_jogados += 1
        return True  # Jogada realizada com sucesso

    def desfazer(self, r, c):
        # Desfaz uma jogada (útil para o algoritmo minimax)
        if not self.dentro_limite(r, c) or self.grade[r][c] == VAZIO:
            return False  # Se inválido ou já vazio, retorna False
        self.grade[r][c] = VAZIO
        self.movimentos_jogados -= 1
        return True

    def cheio(self):
        # Verifica se o tabuleiro está cheio
        return self.movimentos_jogados >= self.n * self.n

    def vencedor(self):
        """
        Verifica se há um vencedor usando união de conjuntos (Union-Find).
        A IA vence se ligar os lados esquerdo e direito.
        O humano vence se ligar os lados superior e inferior.
        """
        N = self.n
        tamanho = N * N + 4  # +4 para os "nós virtuais" das bordas
        pai = list(range(tamanho))  # Vetor pai para Union-Find
        rank = [0] * tamanho       # Rank para otimização

        def idx(r,c): return r * N + c  # Converte coordenadas para índice único

        def encontrar(a):  # Função find com compressão de caminho
            while pai[a] != a:
                pai[a] = pai[pai[a]]
                a = pai[a]
            return a

        def unir(a, b):  # Função union com rank
            ra, rb = encontrar(a), encontrar(b)
            if ra == rb:
                return
            if rank[ra] < rank[rb]:
                pai[ra] = rb
            else:
                pai[rb] = ra
                if rank[ra] == rank[rb]:
                    rank[ra] += 1

        # Nós virtuais para as bordas
        AZUL_ESQ = N * N
        AZUL_DIR = N * N + 1
        VERMELHO_SUP = N * N + 2
        VERMELHO_INF = N * N + 3

        # União das células adjacentes do mesmo jogador
        for r in range(N):
            for c in range(N):
                p = self.grade[r][c]
                if p == VAZIO:
                    continue
                id1 = idx(r,c)
                for rr, cc in self.vizinhos(r,c):
                    if self.grade[rr][cc] == p:
                        unir(id1, idx(rr,cc))
                # Conecta bordas aos nós virtuais
                if p == AZUL:
                    if c == 0: unir(id1, AZUL_ESQ)
                    if c == N-1: unir(id1, AZUL_DIR)
                else:
                    if r == 0: unir(id1, VERMELHO_SUP)
                    if r == N-1: unir(id1, VERMELHO_INF)

        # Verifica se algum jogador ganhou
        if encontrar(AZUL_ESQ) == encontrar(AZUL_DIR):
            return AZUL
        if encontrar(VERMELHO_SUP) == encontrar(VERMELHO_INF):
            return VERMELHO
        return None

# -------------------------------------------------------
# Heurística: Avaliação do tabuleiro para o algoritmo Minimax
# -------------------------------------------------------
def avaliar_tabuleiro(tabuleiro, jogador):
    oponente = VERMELHO if jogador == AZUL else AZUL
    vencedor = tabuleiro.vencedor()
    if vencedor == jogador:
        return 1000  # Vitória
    elif vencedor == oponente:
        return -1000  # Derrota

    pontuacao = 0
    n = tabuleiro.n
    for r in range(n):
        for c in range(n):
            p = tabuleiro.grade[r][c]
            if p == jogador:
                pontuacao += 5  # Celula do jogador → +5
                for rr, cc in tabuleiro.vizinhos(r,c):
                    if tabuleiro.grade[rr][cc] == jogador:
                        pontuacao += 2  # Adjacente → +2
            elif p == oponente:
                pontuacao -= 3  # Celula do oponente → -3
    return pontuacao

# -------------------------------------------------------
# Ordena jogadas mais próximas do centro
# -------------------------------------------------------
def ordenar_jogadas(tabuleiro):
    n = tabuleiro.n
    centro = n / 2
    jogadas = tabuleiro.jogadas_possiveis()
    # Ordena jogadas pela distância ao centro
    jogadas.sort(key=lambda mc: (mc[0]-centro)**2 + (mc[1]-centro)**2)
    return jogadas

# -------------------------------------------------------
# Algoritmo Minimax Padrão
# -------------------------------------------------------
def minimax(tabuleiro, profundidade, maximizando, jogador, nos):
    nos[0] += 1  # Contador de nós visitados
    vencedor = tabuleiro.vencedor()
    oponente = VERMELHO if jogador == AZUL else AZUL
    if vencedor == jogador: return 1000, None
    if vencedor == oponente: return -1000, None
    if profundidade == 0 or tabuleiro.cheio():  # Chegou ao limite
        return avaliar_tabuleiro(tabuleiro, jogador), None

    melhor_jogada = None
    if maximizando:  # Turno da IA
        melhor_valor = -float('inf')
        for r,c in ordenar_jogadas(tabuleiro):
            tabuleiro.jogar(r,c,jogador)
            valor,_ = minimax(tabuleiro, profundidade-1, False, jogador, nos)
            tabuleiro.desfazer(r,c)
            if valor > melhor_valor:
                melhor_valor = valor
                melhor_jogada = (r,c)
        return melhor_valor, melhor_jogada
    else:  # Turno do humano
        melhor_valor = float('inf')
        for r,c in ordenar_jogadas(tabuleiro):
            tabuleiro.jogar(r,c,oponente)
            valor,_ = minimax(tabuleiro, profundidade-1, True, jogador, nos)
            tabuleiro.desfazer(r,c)
            if valor < melhor_valor:
                melhor_valor = valor
                melhor_jogada = (r,c)
        return melhor_valor, melhor_jogada

# -------------------------------------------------------
# Algoritmo Minimax com Poda Alfa-Beta
# -------------------------------------------------------
def alfa_beta(tabuleiro, profundidade, alfa, beta, maximizando, jogador, nos):
    nos[0] += 1
    vencedor = tabuleiro.vencedor()
    oponente = VERMELHO if jogador == AZUL else AZUL
    if vencedor == jogador: return 1000, None
    if vencedor == oponente: return -1000, None
    if profundidade == 0 or tabuleiro.cheio():
        return avaliar_tabuleiro(tabuleiro, jogador), None

    melhor_jogada = None
    if maximizando:
        melhor_valor = -float('inf')
        for r,c in ordenar_jogadas(tabuleiro):
            tabuleiro.jogar(r,c,jogador)
            valor,_ = alfa_beta(tabuleiro, profundidade-1, alfa, beta, False, jogador, nos)
            tabuleiro.desfazer(r,c)
            if valor > melhor_valor:
                melhor_valor = valor
                melhor_jogada = (r,c)
            alfa = max(alfa, valor)
            if beta <= alfa:  # Poda
                break
        return melhor_valor, melhor_jogada
    else:
        melhor_valor = float('inf')
        for r,c in ordenar_jogadas(tabuleiro):
            tabuleiro.jogar(r,c,oponente)
            valor,_ = alfa_beta(tabuleiro, profundidade-1, alfa, beta, True, jogador, nos)
            tabuleiro.desfazer(r,c)
            if valor < melhor_valor:
                melhor_valor = valor
                melhor_jogada = (r,c)
            beta = min(beta, valor)
            if beta <= alfa:
                break
        return melhor_valor, melhor_jogada

# -------------------------------------------------------
# Classe da interface gráfica do jogo Hex
# -------------------------------------------------------
class HexGUI:
    def __init__(self, n=5, tamanho_celula=30, margem=100):
        self.n = n
        self.tamanho_celula = tamanho_celula  # Tamanho de cada hexágono
        self.margem = margem  # Margem para desenho
        self.tabuleiro = TabuleiroHex(n)  # Cria tabuleiro
        self.jogador_atual = AZUL
        self.humano = VERMELHO
        self.algoritmo = 'minimax'  # Algoritmo padrão
        self.profundidade = 2
        self.tempo_total_ia = 0  # Tempo acumulado da IA
        self.mostrar_menu()

    def mostrar_menu(self):
        # Menu de configuração do jogo
        self.menu = tk.Tk()
        self.menu.title("Configurações do Jogo")
        tk.Label(self.menu, text="Escolha a profundidade da IA:").pack()
        self.var_profundidade = tk.IntVar(value=2)
        tk.Spinbox(self.menu, from_=1, to=4, textvariable=self.var_profundidade).pack()
        tk.Label(self.menu, text="Escolha o algoritmo:").pack()
        self.var_algoritmo = tk.StringVar(value='minimax')
        tk.Radiobutton(self.menu, text="Minimax", variable=self.var_algoritmo, value='minimax').pack()
        tk.Radiobutton(self.menu, text="Minimax com Alfa-Beta", variable=self.var_algoritmo, value='alfa_beta').pack()
        tk.Button(self.menu, text="Iniciar Jogo", command=self.iniciar_jogo).pack()
        self.menu.mainloop()

    def iniciar_jogo(self):
        # Inicia o jogo após escolha do menu
        self.profundidade = self.var_profundidade.get()
        self.algoritmo = self.var_algoritmo.get()
        self.menu.destroy()

        s = self.tamanho_celula
        h = s * sqrt(3) / 2  # Altura do hexágono
        largura_canvas = int(self.n * 1.5 * s + s/2 + 2*self.margem)
        altura_canvas = int(self.n * 2*h + self.n*h + 2*self.margem)

        self.janela = tk.Tk()
        self.janela.title("Jogo Hex - IA vs Humano")
        self.info = tk.Label(
            self.janela,
            text="Vez: HUMANO | Nós: 0 | Tempo IA: 0.00s | Tempo total IA: 0.00s",
            font=("Arial",12)
        )
        self.info.pack()

        self.canvas = tk.Canvas(self.janela, width=largura_canvas, height=altura_canvas, bg='lightyellow')
        self.canvas.pack()
        self.desenhar_tabuleiro()
        self.canvas.bind("<Button-1>", self.clique)  # Clique do mouse
        self.janela.mainloop()

    def desenhar_tabuleiro(self):
        # Desenha o tabuleiro com cores dos jogadores
        self.canvas.delete("all")
        s = self.tamanho_celula
        h = s * sqrt(3) / 2
        for r in range(self.n):
            for c in range(self.n):
                x = self.margem + c*1.5*s
                y = self.margem + r*2*h + c*h
                cor = 'white'
                if self.tabuleiro.grade[r][c] == AZUL: cor = 'blue'
                elif self.tabuleiro.grade[r][c] == VERMELHO: cor = 'red'
                self.desenhar_hex(x, y, s, cor)

    def desenhar_hex(self, x, y, s, cor):
        # Desenha um hexágono em (x,y) com tamanho s e cor
        h = s * sqrt(3) / 2
        pontos = [
            x+s, y,
            x+s/2, y+h,
            x-s/2, y+h,
            x-s, y,
            x-s/2, y-h,
            x+s/2, y-h
        ]
        self.canvas.create_polygon(pontos, fill=cor, outline='black', width=2)

    def clique(self, evento):
        # Detecta clique do humano e faz jogada
        s = self.tamanho_celula
        h = s * sqrt(3) / 2
        x_click, y_click = evento.x, evento.y
        for r in range(self.n):
            for c in range(self.n):
                x = self.margem + c*1.5*s
                y = self.margem + r*2*h + c*h
                dx = abs(x_click - x)
                dy = abs(y_click - y)
                if dx <= s*0.9 and dy <= h*0.9:
                    if self.tabuleiro.jogar(r,c,self.humano):
                        self.apos_jogada()
                    return

    def apos_jogada(self):
        # Verifica se alguém ganhou e executa turno da IA
        vencedor = self.tabuleiro.vencedor()
        self.desenhar_tabuleiro()
        if vencedor:
            messagebox.showinfo("Fim de Jogo", f"Vencedor: {vencedor}")
            self.reiniciar_jogo()
            return

        # Turno da IA
        nos = [0]  # Contador de nós visitados
        inicio = time.time()
        if self.algoritmo == 'minimax':
            _, jogada = minimax(self.tabuleiro, self.profundidade, True, AZUL, nos)
        else:
            _, jogada = alfa_beta(self.tabuleiro, self.profundidade, -float('inf'), float('inf'), True, AZUL, nos)
        fim = time.time()

        tempo_jogada_ia = fim - inicio
        self.tempo_total_ia += tempo_jogada_ia  # Soma tempo da IA

        if jogada:
            self.tabuleiro.jogar(jogada[0], jogada[1], AZUL)
        self.desenhar_tabuleiro()

        vencedor = self.tabuleiro.vencedor()
        if vencedor:
            messagebox.showinfo("Fim de Jogo", f"Vencedor: {vencedor}")
            self.reiniciar_jogo()

        self.info.config(
            text=f"Vez: HUMANO | Nós visitados: {nos[0]} | Tempo IA: {tempo_jogada_ia:.2f}s | Tempo total IA: {self.tempo_total_ia:.2f}s"
        )

    def reiniciar_jogo(self):
        # Reinicia o tabuleiro e tempo da IA
        self.tabuleiro = TabuleiroHex(self.n)
        self.tempo_total_ia = 0
        self.desenhar_tabuleiro()
        self.info.config(text="Vez: HUMANO | Nós: 0 | Tempo IA: 0.00s | Tempo total IA: 0.00s")

# -------------------------------------------------------
# Executa o jogo
# -------------------------------------------------------
if __name__ == "__main__":
    HexGUI(5)  # Inicializa a interface com tabuleiro 5x5
