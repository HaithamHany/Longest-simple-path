import heapq
import math
from PriorityQueueNode import PriorityQueueNode

from DFS import DFS
from Graph import Graph


class Heuristics:
    def __init__(self, graph, lcc):
        self.graph = graph
        self.lcc = set(lcc)  # Store the LCC as a set for quick lookup

    def euclidean_distance(self, coord1, coord2):
        return math.sqrt((coord1[0] - coord2[0]) ** 2 + (coord1[1] - coord2[1]) ** 2)

    def modified_heuristic(self, current, target):
        return 1 / (1 + self.euclidean_distance(self.graph.get_coordinates(current),
                                                self.graph.get_coordinates(target)))

    def edge_length(self, u, v):
        coord_u = self.graph.get_coordinates(u)
        coord_v = self.graph.get_coordinates(v)
        return self.euclidean_distance(coord_u, coord_v)

    def aStar_longest_path(self, s, d):
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
                    path = self.aStar_longest_path(start_vertex, end_vertex)
                    if path:
                        path_length = sum(self.edge_length(path[i], path[i + 1]) for i in range(len(path) - 1))
                        if path_length > longest_path_length:
                            longest_path_length = path_length
                            longest_path = path

        return longest_path_length, longest_path

    def ida_star_longest_path(self, start, goal):
        if start not in self.lcc or goal not in self.lcc:
            return None

        threshold = 0  # Start with a low threshold since we are maximizing
        path = [start]
        visited = set(path)

        while True:
            temp = self.search(path, 0, threshold, goal, visited)
            if isinstance(temp, list):
                return temp
            if temp == float('-inf'):
                return None
            threshold = temp

    def search(self, path, g, threshold, goal, visited):
        current = path[-1]
        f = g - self.modified_heuristic(current, goal)

        if f > threshold:
            return f
        if current == goal:
            return path

        max_cost = float('-inf')
        for neighbor in self.graph.vertices[current]:
            if neighbor in self.lcc and neighbor not in visited:
                path.append(neighbor)
                visited.add(neighbor)
                t = self.search(path, g + self.edge_length(current, neighbor), threshold, goal, visited)
                if isinstance(t, list):
                    return t
                if t > max_cost:
                    max_cost = t
                path.pop()
                visited.remove(neighbor)

        return max_cost

    def find_longest_path_ida_star(self):
        longest_path = []
        longest_path_length = 0
        checked_pairs = set()  # Set to track checked start-goal pairs

        for start in self.lcc:
            for goal in self.lcc:
                if start != goal and (start, goal) not in checked_pairs:
                    # Add both directions to the set because path length from start to goal is the same as from goal to start
                    checked_pairs.add((start, goal))
                    checked_pairs.add((goal, start))

                    path = self.ida_star_longest_path(start, goal)
                    if path:
                        path_length = len(path) - 1  # Length in terms of number of edges
                        if path_length > longest_path_length:
                            longest_path_length = path_length
                            longest_path = path

        return longest_path_length, longest_path


#Example
#g = Graph()
#g.read_edges_from_file('self.graph.Edges.txt')
#dfs = DFS(g)
#lcc = dfs.DFS_LCC()
#h = Heuristics(g, lcc)

#s, d = lcc[0], lcc[-1]  # example vertices
#lsp_path = h.aStar_longest_path(s, d)
#print("Longest Simple Path:", lsp_path)

#start, goal = lcc[0], lcc[-1]

#ida_path = h.ida_star_longest_path(start, goal)
#print("IDA* Longest Simple Path:", ida_path#
