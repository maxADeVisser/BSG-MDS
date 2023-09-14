class AdjacencyMatrix:
    # HAVENT TESTED IT PROPERLY
    # undirected unweighted adjacency matrix
    def __init__(self, size: int) -> None:
        self.matrix = []
        self.size = size

        for i in range(size):
            self.matrix.append([0 for j in range(size)])

    def add_edge(self, v1, v2):
        self.matrix[v1][v2] = 1
        self.matrix[v2][v1] = 1
