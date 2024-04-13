import math
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
        if u in self.vertices and v in self.vertices:
            if v not in self.vertices[u]:
                self.vertices[u].append(v)
            if u not in self.vertices[v]:
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

    def generate_random_geometric_graph(self, n, r):
        """Generate a random geometric graph with n vertices and connection radius r."""
        self.vertices = {}
        self.coordinates = {}

        # Add vertices
        for i in range(n):
            self.add_vertex(i)

        # Add edges
        for u in self.vertices:
            for v in self.vertices:
                if u != v and self.euclidean_distance(self.coordinates[u], self.coordinates[v]) < r:
                    self.add_edge(u, v)

    def euclidean_distance(self, coord1, coord2):
        """Calculate the Euclidean distance between two coordinates."""
        return math.sqrt((coord1[0] - coord2[0]) ** 2 + (coord1[1] - coord2[1]) ** 2)

    def write_to_file(self, file_path):
        with open(file_path, 'w') as file:
            for vertex, edges in self.vertices.items():
                ux, uy = self.coordinates[vertex]
                for edge in edges:
                    if vertex < edge:  # Ensure each edge is written only once
                        vx, vy = self.coordinates[edge]
                        file.write(f"{vertex} {ux} {uy} {edge} {vx} {vy}\n")

    def read_edges_with_coordinates_from_file(self, file_path):
        with open(file_path, 'r') as file:
            for line in file:
                # Expecting each line to have the format: u x1 y1 v x2 y2
                parts = line.strip().split()
                u, (x1, y1), v, (x2, y2) = int(parts[0]), (float(parts[1]), float(parts[2])), int(parts[3]), (
                float(parts[4]), float(parts[5]))

                # Add vertices with coordinates if they don't already exist
                if u not in self.vertices:
                    self.add_vertex_with_coordinates(u, (x1, y1))
                if v not in self.vertices:
                    self.add_vertex_with_coordinates(v, (x2, y2))

                # Add edge between u and v
                self.add_edge(u, v)

    def add_vertex_with_coordinates(self, v, coords):
        if v not in self.vertices:
            self.vertices[v] = []
            self.coordinates[v] = coords

    def generate_random_geometric_graph_full(self, n ,r):
        self.generate_random_geometric_graph(n, r)
        self.write_to_file('random_geometric_graph_OUTPUT.edges')
        self.read_edges_with_coordinates_from_file('random_geometric_graph_OUTPUT.edges')





#g = Graph()
#radius = 0.1  # You would find the correct r value as per your requirements
#number_of_vertices = 300  # As an example
#g.generate_random_geometric_graph(10, 0.1)
#g.write_to_file('random_geometric_graph_TEST.edges')