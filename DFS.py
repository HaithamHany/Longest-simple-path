from collections import defaultdict
import math
from random import choice

from Graph import Graph


class DFS:
    def __init__(self, graph):
        self.graph = graph
        self.color = {}
        self.predecessor = {}
        self.time = 0
        self.lsp_length = 0
        self.lsp_path = []

    def reset_vertices(self):
        for v in self.graph.vertices:
            self.color[v] = "WHITE"
            self.predecessor[v] = None

    def DFS_LCC(self):
        self.reset_vertices()
        largest_component = []
        for v in self.graph.vertices:
            if self.color[v] == "WHITE":
                component = []
                self.dfs_visit(v, component=component)  # Use dfs_visit to explore component
                if len(component) > len(largest_component):
                    largest_component = component
        return largest_component

    def dfs_visit(self, vertex, current_length=0, current_path=None, component=None):
        self.color[vertex] = 'GRAY'
        if component is not None:
            component.append(vertex)
        if current_path is not None:
            current_path.append(vertex)
            current_length += 1
            if current_length > self.lsp_length:
                self.lsp_length = current_length
                self.lsp_path = list(current_path)

        for next_vertex in self.graph.vertices[vertex]:
            if self.color[next_vertex] == 'WHITE':
                self.predecessor[next_vertex] = vertex
                self.dfs_visit(next_vertex, current_length, current_path, component)

        self.color[vertex] = 'BLACK'  #indicate full exploration of this vertex
        if current_path is not None:
            current_path.pop()

    def find_lsp(self):
        largest_component = self.DFS_LCC()
        self.lsp_length = 0
        self.lsp_path = []

        for start_vertex in largest_component:
            self.reset_vertices()
            self.dfs_visit(start_vertex, current_path=[])

        return self.lsp_length - 1, self.lsp_path

"""
# Example usage
g = Graph()
g.read_edges_from_file('graph.Edges.txt')


dfs = DFS(g)
lcc = dfs.DFS_LCC()
print("Largest Connected Component:", lcc)
lsp_length, lsp_path = dfs.find_lsp()
print("Longest Simple Path Length:", lsp_length)
print("Longest Simple Path:", lsp_path)
"""

