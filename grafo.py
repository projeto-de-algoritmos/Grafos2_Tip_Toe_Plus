import heapq
#cria estrutura de dados para o grafo com matriz de adjacencia
class Graph:
    def __init__(self, num_vertices):
        self.num_vertices = num_vertices
        self.adj_matrix = [[0] * num_vertices for _ in range(num_vertices)]
        self.visited = [False] * num_vertices
    
    def addEdge(self, v1, v2):
        self.adj_matrix[v1][v2] = 1
        self.adj_matrix[v2][v1] = 1
    
    def removeEdge(self, v1, v2):
        self.adj_matrix[v1][v2] = 0
        self.adj_matrix[v2][v1] = 0
    
    def remove_all_edges(self, v):
        for i in range(self.num_vertices):
            self.removeEdge(v, i)
    
    def clearVisited(self):
        self.visited = [False] * self.num_vertices

    #tranforma matriz em grafo
    def matrixToGraph(self, matrix):
        element = 0
        for i in range(len(matrix)):
            for j in range(len(matrix[i])):
                if matrix[i][j] != 7:
                    self.addEdge(element, element)
                    # checa se é possivel ir para a direita, esquerda, cima ou baixo
                    if i+1 < len(matrix) and matrix[i+1][j] != 7:
                        self.addEdge(element, len(matrix[i])+element)
                    if j+1 < len(matrix[i]) and matrix[i][j+1] != 7:
                        self.addEdge(element, element+1)
                    if i-1 >= 0 and matrix[i-1][j] != 7:
                        self.addEdge(element, element-len(matrix[i]))
                    if j-1 >= 0 and matrix[i][j-1] != 7:
                        self.addEdge(element, element-1)
                element += 1

    def removeBlock(self, index):
        for i in range(len(self.adj_matrix)):
            # limpa linha do index 
            self.adj_matrix[index][i] = 0
            # limpa coluna do index
            self.adj_matrix[i][index] = 0

    # cria caminho entre dois pontos usando busca em profundidade
    def dijkstra(self, start, end):
        self.visited = [False] * self.num_vertices
        dist = [float('inf')] * self.num_vertices
        pred = [-1] * self.num_vertices
        dist[start] = 0
        heap = [(0, start)]

        while heap:
            (min_dist, current_vertex) = heapq.heappop(heap)
            if self.visited[current_vertex]:
                continue
            self.visited[current_vertex] = True

            for neighbor in range(self.num_vertices):
                if (self.adj_matrix[current_vertex][neighbor] != 0 and not self.visited[neighbor]
                    and dist[current_vertex] + self.adj_matrix[current_vertex][neighbor] < dist[neighbor]):
                    dist[neighbor] = dist[current_vertex] + self.adj_matrix[current_vertex][neighbor]
                    pred[neighbor] = current_vertex
                    heapq.heappush(heap, (dist[neighbor], neighbor))

        path = []
        
        while current_vertex != start:
            path.insert(0, current_vertex)
            current_vertex = pred[current_vertex]
        path.insert(0, start)

        return path
    
    # transforma caminho em lista de coordenadas
    def pathToCoordinates(self, path, matrix):
        coordinates = []
        for i in path:
            coordinates.append(self.indexToCoordinates(i, matrix))
        return coordinates
    
    # transforma indice em coordenadas
    def indexToCoordinates(self, index, matrix):
        row = int(index) // len(matrix)
        column = index % len(matrix)
        return (row, column)
    
    # transforma coordenadas em indice
    def coordinatesToIndex(self, coordinates, matrix):
        return coordinates[1]*len(matrix) + coordinates[0]
    
    # transforma caminho em lista de movimentos
    def pathToMoves(self, path, matrix):
        moves = []
        if path != None:
            for i in range(len(path)-1):
                moves.append(self.getMove(path[i], path[i+1], matrix))
        return moves

    # retorna movimento entre dois pontos
    def getMove(self, start, end, matrix):
        start = self.indexToCoordinates(start, matrix)
        end = self.indexToCoordinates(end, matrix)
        if start[0] == end[0]:
            if start[1] > end[1]:
                return [-1, 0]
            else:
                return [1, 0]
        else:
            if start[0] > end[0]:
                return [0, -1]
            else:
                return [0, 1]
