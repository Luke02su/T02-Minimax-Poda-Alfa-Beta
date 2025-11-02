# Relatório Técnico – Inteligência artificial aplicada ao Jogo Hexagonal com Minimax e Poda Alfa-Beta

Autor: Lucas Samuel Dias
Professor(a):Dr. Danielle
Discipina: Integência Computacional e Artificial

## 1.Introdução

  Este relatório técnico tem como objetivo apresentar a análise, desenvolvimento e funcionamento de um sistema de inteligência artificial (IA) aplicado ao jogo hexagonal desenvolvido em Python. O projeto foi concebido para demonstrar o uso dos algoritmos Minimax e Poda Alfa-Beta, amplamente utilizados em jogos de estratégia para tomada de decisão autônoma. O foco do trabalho é compreender como esses algoritmos se comportam em diferentes profundidades e o impacto da heurística no desempenho.

## 2. Desenvolvimento

### 2.1 Estrutura do Sistema

  O sistema foi implementado em Python, utilizando uma interface gráfica que representa um tabuleiro hexagonal. Cada célula do tabuleiro corresponde a uma posição válida de jogo, e as jogadas são realizadas alternadamente entre o jogador humano e a IA. Durante o jogo, são destacados os nós visitados pela IA e o tempo gasto em cada jogada, o que permite uma análise visual e quantitativa do desempenho.

### 2.2 Algoritmo Minimax

  O algoritmo Minimax é uma técnica clássica utilizada em jogos de soma zero, em que dois jogadores competem entre si. Ele simula todas as jogadas possíveis até uma profundidade determinada e avalia o valor de cada estado final com base em uma função heurística e prioridade. A IA escolhe o movimento que maximiza suas chances de vitória, assumindo que o oponente jogará de forma ótima.

### 2.3 Poda Alfa-Beta

  A Poda Alfa-Beta é uma otimização do Minimax que reduz significativamente o número de nós analisados. Ela elimina ramos da árvore de decisão que não podem alterar o resultado final, mantendo o mesmo resultado do Minimax, mas com muito melhor desempenho. Esse método é essencial para permitir profundidades maiores sem comprometer a velocidade de resposta da IA.

### 2.4 Comparação de Desempenho

  Foram realizados testes comparativos entre o Minimax e a Poda Alfa-Beta, variando a profundidade de busca de 1 a 4 níveis. Observou-se que o Minimax apresenta um crescimento exponencial no tempo de processamento, enquanto a Poda Alfa-Beta mantém tempos muito mais baixos devido à eliminação de ramos desnecessários. A seguir, uma análise qualitativa dos resultados:
- Profundidade 1: ambos os algoritmos apresentam resposta imediata.
- Profundidade 2: diferença pequena, mas a poda já começa a ser perceptível.
- Profundidade 3: o Minimax apresenta lentidão significativa, enquanto a Poda Alfa-Beta mantém boa fluidez.
- Profundidade 4: o Minimax torna-se praticamente inviável em tempo real, enquanto a Poda Alfa-Beta ainda opera dentro de limites aceitáveis.

### 2.5 Função Heurística

  A função heurística de avaliação implementada avalia o estado atual do tabuleiro com base em critérios como número de posições ocupadas e proximidade da vitória. Essa heurística permite à IA estimar o quão favorável é uma situação, mesmo sem explorar todas as possibilidades até o fim da partida.

### 2.6 Medição de Desempenho da IA

  Durante o jogo, é calculado o tempo de execução exclusivamente das jogadas da IA. O sistema acumula o tempo total gasto pela IA ao longo da partida, fornecendo uma métrica precisa de desempenho. Além disso, são exibidos os nós visitados em cada jogada, auxiliando na visualização da complexidade do algoritmo em ação.

### 2.7 Interface Gráfica

  A interface gráfica utiliza uma representação hexagonal organizada, onde cada célula é desenhada de forma a evitar sobreposições. As jogadas da IA e do jogador humano são destacadas visualmente, e os nós visitados são indicados em tempo real, tornando o processo de tomada de decisão da IA compreensível ao observador.

## 3 Conclusão

  O projeto demonstrou com sucesso a aplicação dos algoritmos Minimax e Poda Alfa-Beta no contexto de um jogo hexagonal interativo. A análise confirmou que, embora o Minimax produza decisões corretas, seu custo computacional cresce rapidamente com a profundidade. Já a Poda Alfa-Beta mantém o mesmo resultado lógico, porém com desempenho muito superior. A inclusão da heurística e da medição de tempo da IA proporcionou uma visão mais profunda sobre a eficiência do processo de decisão. Como trabalho futuro, propõe-se a inclusão de heurísticas adaptativas e otimização adicional para busca mais profunda sem perda de desempenho.

O projeto demonstrou com sucesso a aplicação dos algoritmos Minimax e Poda Alfa-Beta no contexto de um jogo hexagonal interativo. A análise confirmou que, embora o Minimax produza decisões corretas, seu custo computacional cresce rapidamente com a profundidade. Já a Poda Alfa-Beta mantém o mesmo resultado lógico, porém com desempenho muito superior. A inclusão da heurística e da medição de tempo da IA proporcionou uma visão mais profunda sobre a eficiência do processo de decisão. Como trabalho futuro, propõe-se a inclusão de heurísticas adaptativas e otimização adicional para busca mais profunda sem perda de desempenho.
