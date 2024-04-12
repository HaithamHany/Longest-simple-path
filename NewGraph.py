import random


class Graph:
    def __init__(self):
        self.vertices = {}
        self.coordinates = {}

    def add_vertex(self, v):
        if v not in self.vertices:
            x = random.random()  # Random x-coordinate between 0 and 1
            y = random.random()  # Random y-coordinate between 0 and 1
            self.vertices[v] = []
            self.coordinates[v] = (x, y)


    def add_edge(self, u, v):
            if u in self.vertices:
                self.vertices[u].append(v)
            if v in self.vertices:
                self.vertices[v].append(u)

    def get_coordinates(self, vertex):
        return self.coordinates.get(vertex, (None, None))  # Return None if vertex doesn't exist

    def read_edges_from_file(self, file_path):
        with open(file_path, 'r') as file:
            for line in file:
                u, v = map(int, line.strip().split())  # Adjust split() accordingly if using a different delimiter
                if u not in self.vertices:
                    self.add_vertex(u)
                if v not in self.vertices:
                    self.add_vertex(v)
                self.add_edge(u, v)

# New method to initialize or reset vertex properties
    def initialize_vertex_properties(self):
        self.vertex_properties = {v: {'color': 'WHITE', 'd': 0, 'f': 0, 'pi': None} for v in self.vertices}


