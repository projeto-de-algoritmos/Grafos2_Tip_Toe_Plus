import heapq

#grafo com dicionario de adjacencia e pesos nas arestas
class Graph:
    def __init__(self, num_vertices):
        self.vertices = {}
        self.num_vertices = num_vertices

    def addEdge(self, v1, v2, weight):
        if v1 not in self.vertices:
            self.vertices[v1] = []
        self.vertices[v1].append((v2, weight))
    
    def removeEdge(self, v1, v2):
        if v1 in self.vertices:
            for i in range(len(self.vertices[v1])):
                if self.vertices[v1][i][0] == v2:
                    self.vertices[v1].pop(i)
                    break
        if v2 in self.vertices:
            for i in range(len(self.vertices[v2])):
                if self.vertices[v2][i][0] == v1:
                    self.vertices[v2].pop(i)
                    break
    
    def matrixToGraph(self, matrix):
        element = 0
        for i in range(len(matrix)):
            for j in range(len(matrix[i])):
                if matrix[i][j] != 7:
                    self.addEdge(element, element, 0)
                    # checa se é possivel ir para a direita, esquerda, cima ou baixo
                    if i+1 < len(matrix) and matrix[i+1][j] != 7:
                        self.addEdge(element, len(matrix[i])+element, matrix[i+1][j])
                    if j+1 < len(matrix[i]) and matrix[i][j+1] != 7:
                        self.addEdge(element, element+1, matrix[i][j+1])
                    if i-1 >= 0 and matrix[i-1][j] != 7:
                        self.addEdge(element, element-len(matrix[i]), matrix[i-1][j])
                    if j-1 >= 0 and matrix[i][j-1] != 7:
                        self.addEdge(element, element-1, matrix[i][j-1])
                element += 1
    
    def removeBlock(self, index):
        if index in self.vertices:
            self.vertices[index] = []
    
    # cria caminho entre dois pontos usando dijkstra
    def dijkstra(self, start, end):
        dist = [float('inf')] * self.num_vertices
        pred = [-1] * self.num_vertices
        dist[start] = 0
        heap = [(0, start)]
        while heap:
            (min_dist, current_vertex) = heapq.heappop(heap)
            for neighbor, weight in self.vertices[current_vertex]:
                if dist[current_vertex] + weight < dist[neighbor]:
                    dist[neighbor] = dist[current_vertex] + weight
                    pred[neighbor] = current_vertex
                    heapq.heappush(heap, (dist[neighbor], neighbor))
        path = []
        current_vertex = end
        while current_vertex != -1:
            path.append(current_vertex)
            current_vertex = pred[current_vertex]
        return path
    
    def pathToCoordinates(self, path, matrix):
        coordinates = []
        for i in range(len(path)):
            coordinates.append((path[i] % len(matrix[0]), path[i] // len(matrix[0])))
        return coordinates
    
    def indexToCoordinates(self, index, matrix):
        return (index % len(matrix[0]), index // len(matrix[0]))
    
    def coordinatesToIndex(self, coordinates, matrix):
        return coordinates[0] + coordinates[1] * len(matrix[0])
    
    def pathToMoves(self, path, matrix):
        moves = []
        for i in range(len(path)-1):
            if path[i+1] - path[i] == 1:
                moves.append([-1, 0])
            elif path[i+1] - path[i] == -1:
                moves.append([1, 0])
            elif path[i+1] - path[i] == len(matrix[0]):
                moves.append([0, -1])
            elif path[i+1] - path[i] == -len(matrix[0]):
                moves.append([0, 1])
        return moves
    
    def getMoves(self, start, end, matrix):
        path = self.dijkstra(start, end)
        return self.pathToMoves(path, matrix)