import heapq
import math

from DFS import DFS
from NewGraph import Graph


class Heuristics:
    def __init__(self, graph):
        self.graph = graph

    def aStar_longest_path(self, s, d):
        # Initialize the distances and heuristics
        distances = {vertex: float('-inf') for vertex in self.graph.vertices}
        heuristic = {vertex: self.euclidean_distance(self.graph.get_coordinates(vertex), self.graph.get_coordinates(d)) for vertex in self.graph.vertices}
        distances[s] = 0

        # Priority queue
        queue = []
        heapq.heappush(queue, (-(distances[s] + heuristic[s]), s))  # Use negative for max-heap simulation

        # Set of visited nodes to avoid revisiting
        visited = set()

        # Predecessor map to reconstruct the path later
        predecessor = {vertex: None for vertex in self.graph.vertices}

        while queue:
            _, current = heapq.heappop(queue)
            visited.add(current)

            # Break early if destination is reached
            if current == d:
                break

            # Explore neighbors
            for neighbor in self.graph.vertices[current]:
                if neighbor not in visited:
                    new_distance = distances[current] + self.edge_length(current, neighbor)
                    if new_distance > distances[neighbor]:
                        distances[neighbor] = new_distance
                        predecessor[neighbor] = current
                        priority = -(new_distance + heuristic[neighbor])
                        heapq.heappush(queue, (priority, neighbor))

        # Reconstruct the path from s to d
        path = []
        step = d
        while step is not None:
            path.append(step)
            step = predecessor[step]
        path.reverse()

        return path

    def euclidean_distance(self, coord1, coord2):
        return math.sqrt((coord1[0] - coord2[0])**2 + (coord1[1] - coord2[1])**2)

    def edge_length(self, u, v):
        coord_u = self.graph.get_coordinates(u)
        coord_v = self.graph.get_coordinates(v)
        return self.euclidean_distance(coord_u, coord_v)

    def ida_star_longest_path(self, start, goal):
        threshold = self.euclidean_distance(self.graph.get_coordinates(start), self.graph.get_coordinates(goal))

        # Start from the initial node
        path = [start]
        visited = set(path)

        while True:
            temp = self.search(path, 0, threshold, goal, visited)
            if isinstance(temp, list):  # If a result path is returned
                return temp
            if temp == float('inf'):  # If no path is found and we've exhausted the search space
                return None
            threshold = temp  # Update the threshold

    def search(self, path, g, threshold, goal, visited):
        current = path[-1]
        f = g + self.euclidean_distance(self.graph.get_coordinates(current), self.graph.get_coordinates(goal))

        # Check if current f exceeds the threshold
        if f > threshold:
            return f

        # Goal check
        if current == goal:
            return path

        # Set minimum cost estimate for the next iteration
        min_cost = float('inf')

        # Explore each neighbor
        for neighbor in self.graph.vertices[current]:
            if neighbor not in visited:
                path.append(neighbor)
                visited.add(neighbor)
                t = self.search(path, g + self.edge_length(current, neighbor), threshold, goal, visited)

                if isinstance(t, list):  # Path found
                    return t
                if t < min_cost:  # Update minimum cost
                    min_cost = t

                # Backtrack
                path.pop()
                visited.remove(neighbor)

        return min_cost

#Example
g = Graph()
g.read_edges_from_file('graph.Edges.txt')
h = Heuristics(g)

dfs = DFS(g)
lcc = dfs.DFS_LCC()
s, d = lcc[0], lcc[-1]  # example vertices
lsp_path = h.aStar_longest_path(s, d)
print("Longest Simple Path:", lsp_path)

start, goal = lcc[0], lcc[-1]

ida_path = h.ida_star_longest_path(start, goal)
print("IDA* Longest Simple Path:", ida_path)
