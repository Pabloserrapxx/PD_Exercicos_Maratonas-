import math
from collections import defaultdict

# Função para adicionar uma aresta ao grafo
def adicionar_aresta(grafo, u, v, w):
    grafo[u].append((v, w))
    grafo[v].append((u, w))

# Função DFS para calcular a distância mínima
def dfs(grafo, v, r, imposto, visitados):
    visitados.add(v)
    dist_total = 0
    imposto_total = imposto[v-1]

    # Percorre todos os filhos de v
    for u, w in grafo[v]:
        if u not in visitados:
            dist, imposto_na_subarvore = dfs(grafo, u, r, imposto, visitados)
            imposto_total += imposto_na_subarvore
            viagens = math.ceil(imposto_na_subarvore / r)
            dist_total += dist + 2 * viagens * w

    return dist_total, imposto_total

# Função para criar o grafo com base nas conexões fornecidas
def criar_grafo(conexoes):
    grafo = defaultdict(list)
    for u, v, w in conexoes:
        adicionar_aresta(grafo, u, v, w)
    return grafo

# Função para solicitar ao usuário as informações sobre as cidades e conexões
def obter_entrada():
    n, r = map(int, input().split())
    imposto = list(map(int, input().split()))
    conexoes = []

    for _ in range(n - 1):
        u, v, w = map(int, input().split())
        conexoes.append((u, v, w))

    return n, r, imposto, conexoes

# Função principal para resolver o problema
def coletar_impostos(n, r, imposto, conexoes):
    grafo = criar_grafo(conexoes)
    visitados = set()

    # Inicia a DFS pela raiz da árvore
    distancia_minima, _ = dfs(grafo, 1, r, imposto, visitados)
    return distancia_minima

# Solicitar entrada ao usuário
n, r, imposto, conexoes = obter_entrada()

# Calcula a distância mínima
distancia_minima = coletar_impostos(n, r, imposto, conexoes)
print(distancia_minima)
