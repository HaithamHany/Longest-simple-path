import random


class Grasp:
    def __init__(self, graph, lcc):
        self.graph = graph  # Full graph with vertices and neighbors
        self.lcc = set(lcc)  # Set of vertices in the largest connected component (LCC)
        self.iterations = 20
        self.candidate_list_size = 3

    def get_candidates(self, current_node, path):
        # Collect nodes that are not already in the path and are within the LCC to avoid cycles
        candidates = [
            node for node in self.graph.vertices[current_node]
            if node not in path and node in self.lcc
        ]
        # Convert neighbors list and LCC list to sets and calculate intersection
        candidates.sort(key=lambda x: len(set(self.graph.vertices[x]) & self.lcc), reverse=True)
        # Return top candidates based on candidate_list_size
        return candidates[:self.candidate_list_size]

    def greedy_randomized_construction(self):
        if not self.lcc:
            return []  # Return an empty path if there are no vertices in the LCC

        # Start from a random node in the LCC
        start_node = random.choice(list(self.lcc))
        path = [start_node]
        current_node = start_node

        while True:
            candidates = self.get_candidates(current_node, path)
            if not candidates:
                break
            # Select one candidate randomly from the candidates list
            next_node = random.choice(candidates)
            path.append(next_node)
            current_node = next_node

        return path

    def local_search(self, path):
        # Try to improve the path by checking if any node not in the path can be inserted
        best_path = path
        for i in range(len(path) - 1):
            for node in self.lcc:
                if node not in path:
                    # Check if inserting the node between any two consecutive nodes in the path is possible
                    if node in self.graph.vertices[path[i]] and node in self.graph.vertices[path[i + 1]]:
                        # Create a new path with the node inserted
                        new_path = path[:i + 1] + [node] + path[i + 1:]
                        # Check if the new path is simple (no cycles) and longer than the best path
                        if len(new_path) > len(best_path) and self.verify_simple_path(new_path):
                            best_path = new_path
        return best_path

    def verify_simple_path(self, path):
        # Verify that the path does not contain repeated nodes (no cycles)
        return len(path) == len(set(path))

    def grasp_longest_path(self):
        best_path = []
        for _ in range(self.iterations):
            path = self.greedy_randomized_construction()
            path = self.local_search(path)

            # Verify the path is simple before considering it
            if self.verify_simple_path(path):
                # Check if the path is entirely within the LCC
                if set(path).issubset(self.lcc):
                    if len(path) > len(best_path):
                        best_path = path
                else:
                    # If path is not within LCC, skip it
                    continue

        return best_path