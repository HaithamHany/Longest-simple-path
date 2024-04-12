import heapq
import math

from DFS import DFS
from NewGraph import Graph

class Heuristics:
    def __init__(self, graph, lcc):
        self.graph = graph
        self.lcc = set(lcc)  # Store the LCC as a set for quick lookup

    def euclidean_distance(self, coord1, coord2):
        return math.sqrt((coord1[0] - coord2[0]) ** 2 + (coord1[1] - coord2[1]) ** 2)

    def edge_length(self, u, v):
        coord_u = self.graph.get_coordinates(u)
        coord_v = self.graph.get_coordinates(v)
        return self.euclidean_distance(coord_u, coord_v)

    def aStar_longest_path(self, s, d):
        if s not in self.lcc or d not in self.lcc:
            return None  # Ensure both s and d are in the LCC

        # Initialize distances and heuristics limited to the LCC
        distances = {vertex: float('-inf') for vertex in self.lcc}
        heuristic = {vertex: self.euclidean_distance(self.graph.get_coordinates(vertex), self.graph.get_coordinates(d))
                     for vertex in self.lcc}
        distances[s] = 0

        # Priority queue
        queue = []
        heapq.heappush(queue, (-(distances[s] + heuristic[s]), s))

        # Set of visited nodes to avoid revisiting
        visited = set()

        # Predecessor map to reconstruct the path later
        predecessor = {vertex: None for vertex in self.lcc}

        while queue:
            _, current = heapq.heappop(queue)
            visited.add(current)
            if current == d:
                break

            # Explore neighbors within the LCC
            for neighbor in self.graph.vertices[current]:
                if neighbor in self.lcc and neighbor not in visited:
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

    def ida_star_longest_path(self, start, goal):
        """Find the longest simple path from start to goal using IDA* within the LCC."""
        if start not in self.lcc or goal not in self.lcc:
            return None  # Ensure start and goal are within the LCC

        threshold = self.euclidean_distance(self.graph.get_coordinates(start), self.graph.get_coordinates(goal))
        path = [start]
        visited = set(path)

        while True:
            temp = self.search(path, 0, threshold, goal, visited)
            if isinstance(temp, list):  # If a valid path is found
                return temp
            if temp == float('inf'):  # If no path found within threshold
                return None
            threshold = temp  # Update the threshold

    def search(self, path, g, threshold, goal, visited):
        """Helper function for IDA* search."""
        current = path[-1]
        f = g + self.euclidean_distance(self.graph.get_coordinates(current), self.graph.get_coordinates(goal))

        # Check if current f value exceeds the threshold
        if f > threshold:
            return f

        # Check if the goal is reached
        if current == goal:
            return path

        # Set minimum cost estimate for the next iteration
        min_cost = float('inf')

        # Explore each neighbor within the LCC
        for neighbor in self.graph.vertices[current]:
            if neighbor in self.lcc and neighbor not in visited:
                path.append(neighbor)
                visited.add(neighbor)
                t = self.search(path, g + self.edge_length(current, neighbor), threshold, goal, visited)

                if isinstance(t, list):  # Path found
                    return t
                if t < min_cost:  # Update minimum cost if new cost is lower
                    min_cost = t

                # Backtrack
                path.pop()
                visited.remove(neighbor)

        return min_cost


#Example
g = Graph()
g.read_edges_from_file('graph.Edges.txt')
dfs = DFS(g)
lcc = dfs.DFS_LCC()
h = Heuristics(g, lcc)

s, d = lcc[0], lcc[-1]  # example vertices
lsp_path = h.aStar_longest_path(s, d)
print("Longest Simple Path:", lsp_path)

start, goal = lcc[0], lcc[-1]

ida_path = h.ida_star_longest_path(start, goal)
print("IDA* Longest Simple Path:", ida_path)
