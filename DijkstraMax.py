import heapq
from Graph import Graph
from PriorityQueueNode import PriorityQueueNode


class DijkstraMax:
    def __init__(self, graph):
        self.graph = graph
        self.Q = []  # Priority queue

    def initialize_single_source_max(self, s):
        self.distances = {v: float('-inf') for v in self.graph.vertices}
        self.predecessors = {v: None for v in self.graph.vertices}
        self.distances[s] = 0
        heapq.heappush(self.Q, PriorityQueueNode(s, 0))

    def relax_max(self, u, v):
        if self.distances[v] < self.distances[u] + 1:
            self.distances[v] = self.distances[u] + 1
            self.predecessors[v] = u
            heapq.heappush(self.Q, PriorityQueueNode(v, self.distances[v]))

    def dijkstra_max(self, s):
        self.initialize_single_source_max(s)
        visited = set()

        while self.Q:
            u = heapq.heappop(self.Q).vertex
            if u in visited:
                continue
            visited.add(u)

            for v in self.graph.vertices[u]:
                if v not in visited:
                    self.relax_max(u, v)

        # Reconstruct the LSP from the distances and predecessors
        end_vertex = max(self.distances, key=self.distances.get)
        path_length = self.distances[end_vertex]  # Length of the longest path
        path = [end_vertex]
        while self.predecessors[end_vertex] is not None:
            path.append(self.predecessors[end_vertex])
            end_vertex = self.predecessors[end_vertex]
        path.reverse()

        return path, path_length  # Return both path and length

    def get_longest_path(self):
        longest_path_length = 0
        longest_path = []

        for v in self.graph.vertices:
            dijkstra_max = DijkstraMax(self.graph)
            path, length = dijkstra_max.dijkstra_max(v)
            if length > longest_path_length:
                longest_path_length = length
                longest_path = path

        return longest_path_length, longest_path


g = Graph()
g.read_edges_from_file('graph.Edges.txt')
d = DijkstraMax(g)
path, length = d.get_longest_path()
print("The Longest Simple Path (LSP) is:", path, "with length:", length)