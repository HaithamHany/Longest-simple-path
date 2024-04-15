import heapq
import math
import random


class aStar:
    def __init__(self, graph, lcc):
        self.graph = graph
        self.lcc = lcc

    def euclidean_distance(self, coord1, coord2):
        return math.sqrt((coord1[0] - coord2[0]) ** 2 + (coord1[1] - coord2[1]) ** 2)

    def modified_heuristic(self, current, target):
        return 1 / (1 + self.euclidean_distance(self.graph.get_coordinates(current),
                                                self.graph.get_coordinates(target)))

    def edge_length(self, u, v):
        coord_u = self.graph.get_coordinates(u)
        coord_v = self.graph.get_coordinates(v)
        return self.euclidean_distance(coord_u, coord_v)

    def a_star_longest_path(self, s, d):
        if s not in self.lcc or d not in self.lcc:
            return None

        distances = {vertex: float('-inf') for vertex in self.lcc}
        heuristic = {vertex: self.modified_heuristic(vertex, d) for vertex in self.lcc}
        distances[s] = 0

        queue = []
        heapq.heappush(queue, (-(distances[s] + heuristic[s]), s))  # Maximize path length

        visited = set()
        predecessor = {vertex: None for vertex in self.lcc}

        while queue:
            _, current = heapq.heappop(queue)
            visited.add(current)
            if current == d:
                break

            for neighbor in self.graph.vertices[current]:
                if neighbor in self.lcc and neighbor not in visited:
                    new_distance = distances[current] + self.edge_length(current, neighbor)
                    if new_distance > distances[neighbor]:
                        distances[neighbor] = new_distance
                        predecessor[neighbor] = current
                        priority = -(new_distance + heuristic[neighbor])  # Higher values are more prioritized
                        heapq.heappush(queue, (priority, neighbor))

        path = []
        step = d
        while step is not None:
            path.append(step)
            step = predecessor[step]
        path.reverse()
        return path

    def find_longest_simple_path(self):
        longest_path = []
        longest_path_length = 0

        for start_vertex in self.lcc:
            for end_vertex in self.lcc:
                if start_vertex != end_vertex:
                    path = self.a_star_longest_path(start_vertex, end_vertex)
                    if path:
                        path_length = sum(self.edge_length(path[i], path[i + 1]) for i in range(len(path) - 1))
                        if path_length > longest_path_length:
                            longest_path_length = path_length
                            longest_path = path

        return longest_path_length, longest_path
