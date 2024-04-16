def encontrar_sequencias(tabuleiro):
    sequencias = []

    # Sequências nas linhas
    for i, linha in enumerate(tabuleiro):
        sequencia_linha = [(i, j) for j, casa in enumerate(linha) if casa in ['.', 'X']]
        sequencias.append(sequencia_linha)

    # Sequências nas colunas
    for j in range(len(tabuleiro[0])):
        sequencia_coluna = [(i, j) for i in range(len(tabuleiro)) if tabuleiro[i][j] in ['.', 'X']]
        sequencias.append(sequencia_coluna)

    # Sequências nas diagonais principais
    for k in range(len(tabuleiro)):
        sequencia_diagonal1 = [(i, k - i) for i in range(max(0, k - len(tabuleiro) + 1), min(k + 1, len(tabuleiro))) if 0 <= k - i < len(tabuleiro) and 0 <= i < len(tabuleiro) and tabuleiro[i][k - i] == '.']
        sequencia_diagonal2 = [(len(tabuleiro) - 1 - i, len(tabuleiro) - 1 - (k - len(tabuleiro) + 1) + i) for i in range(max(0, k - len(tabuleiro) + 1), min(k + 1, len(tabuleiro))) if 0 <= len(tabuleiro) - 1 - (k - len(tabuleiro) + 1) + i < len(tabuleiro) and 0 <= len(tabuleiro) - 1 - i < len(tabuleiro) and tabuleiro[len(tabuleiro) - 1 - i][len(tabuleiro) - 1 - (k - len(tabuleiro) + 1) + i] == '.']
        sequencias.append(sequencia_diagonal1)
        sequencias.append(sequencia_diagonal2)

    # Sequências nas diagonais secundárias
    for k in range(1, 2 * len(tabuleiro) - 1):
        sequencia_diagonal1 = [(i, k - i) for i in range(max(0, k - len(tabuleiro) + 1), min(k + 1, len(tabuleiro))) if 0 <= k - i < len(tabuleiro) and 0 <= i < len(tabuleiro) and tabuleiro[i][k - i] == '.']
        sequencia_diagonal2 = [(len(tabuleiro) - 1 - i, len(tabuleiro) - 1 - (k - len(tabuleiro) + 1) + i) for i in range(max(0, k - len(tabuleiro) + 1), min(k + 1, len(tabuleiro))) if 0 <= len(tabuleiro) - 1 - (k - len(tabuleiro) + 1) + i < len(tabuleiro) and 0 <= len(tabuleiro) - 1 - i < len(tabuleiro) and tabuleiro[len(tabuleiro) - 1 - i][len(tabuleiro) - 1 - (k - len(tabuleiro) + 1) + i] == '.']
        sequencias.append(sequencia_diagonal1)
        sequencias.append(sequencia_diagonal2)

    return sequencias


class GrafoBipartido:
    def __init__(self, sequencias):
        self.sequencias = sequencias
        self.total_vertices = len(sequencias) + 2  # Fonte e sumidouro
        self.grafo = [[0] * self.total_vertices for _ in range(self.total_vertices)]

    def adicionar_aresta(self, u, v, peso):
        self.grafo[u][v] = peso

    def fluxo_maximo(self, origem, destino):
        def bfs():
            fila = [origem]
            visitado = [False] * self.total_vertices
            visitado[origem] = True
            pai = [-1] * self.total_vertices

            while fila:
                u = fila.pop(0)
                for v in range(self.total_vertices):
                    if not visitado[v] and self.grafo[u][v] > 0:
                        fila.append(v)
                        pai[v] = u
                        visitado[v] = True

            return visitado[destino], pai

        fluxo_maximo = 0

        while True:
            existe_caminho, pai = bfs()
            if not existe_caminho:
                break

            fluxo_caminho = float('inf')
            v = destino
            while v != origem:
                u = pai[v]
                fluxo_caminho = min(fluxo_caminho, self.grafo[u][v])
                v = u

            fluxo_maximo += fluxo_caminho

            v = destino
            while v != origem:
                u = pai[v]
                self.grafo[u][v] -= fluxo_caminho
                self.grafo[v][u] += fluxo_caminho
                v = u

        return fluxo_maximo


def torres_pacificas(n, tabuleiro):
    sequencias = encontrar_sequencias(tabuleiro)
    grafo_bipartido = GrafoBipartido(sequencias)
    origem = len(sequencias)
    destino = len(sequencias) + 1

    for i, sequencia in enumerate(sequencias):
        if i < n:
            grafo_bipartido.adicionar_aresta(origem, i, 1)  # Arestas da fonte para as sequências
        else:
            grafo_bipartido.adicionar_aresta(i, destino, 1)  # Arestas das sequências para o sumidouro

        for j, outra_sequencia in enumerate(sequencias):
            if i != j and not interceptam(sequencia, outra_sequencia):
                grafo_bipartido.adicionar_aresta(i, j, 1)  # Arestas entre sequências diferentes que não se interceptam

    return grafo_bipartido.fluxo_maximo(origem, destino)


def interceptam(seq1, seq2):
    for casa1 in seq1:
        for casa2 in seq2:
            if casa1 == casa2:
                return True
    return False


# Solicitar ao usuário para inserir o tabuleiro
n = int(input())
tabuleiro = []

for _ in range(n):
    linha = input().strip()
    tabuleiro.append(linha)

# Calcular e imprimir a saída
saida = torres_pacificas(n, tabuleiro)
print(saida)
