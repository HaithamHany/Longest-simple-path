import random
from Graph import Graph
from Heuristics import Heuristics as h
from math import sqrt

def generate_geometric_graph(n, r):
    """
    Generates a geometric graph with n vertices and adds edges between vertices
    that are within distance r of each other in Euclidean space.

    Parameters:
    n (int): The number of vertices.
    r (float): The maximum distance between nodes for an edge to exist.

    Returns:
    A list of edges in the graph.
    """
    V = [(random.uniform(0, 1), random.uniform(0, 1)) for _ in range(n)]  # List of vertices with random coordinates
    E = []  # List to hold edges

    # Add all undirected edges of length <= r to E
    for i in range(n):
        for j in range(i+1, n):  # Avoid self-loops and check each pair only once
            if (V[i][0] - V[j][0])**2 + (V[i][1] - V[j][1])**2 <= r**2:
                E.append((i+1, j+1))  # Add one since vertex indexing starts at 1

    return E


def create_random_graphs(n, interval):
    left, right = 10, 100   # Max possible distance in a unit square
    success = False

    while right - left > 1e-10:  # Binary search tolerance
        print(f"Tolerance: {right - left}")
        r = (left + right) / 2
        edges = generate_geometric_graph(n, r)
        print(edges[474])

        with open('graph.edges', 'w') as f:
            for edge in edges:
                f.write(f"{edge[0]} {edge[1]}\n")
            f.close()
        graph = Graph(file="graph.edges", verbose=0)
        heuristics = h(graph)
        lcc = heuristics.DFS_LCC()  # Returns the list of nodes in the LCC
        VLCC = sqrt(len(lcc))
        print(VLCC)

        if interval[0] * n <= VLCC <= interval[1] * n:
            success = True
            print(f"Graph with n={n}, r={r:.4f}, VLCC={VLCC:.4f}")
            break
        elif VLCC < interval[0] * n:
            left = r
        else:
            right = r

    if not success:
        print("Failed to generate graph that satisfies the VLCC condition")


def main():
    conditions = [(300, [0.9, 0.95]), (400, [0.8, 0.9]), (500, [0.7, 0.8])]
    create_random_graphs(300, [0.9, 0.95])
    # for n, interval in conditions:
    #     create_random_graphs(n, interval)


if __name__ == '__main__':
    main()
