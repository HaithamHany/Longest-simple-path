import random


def generate_geometric_graph(n, r):
    """
    Generates a geometric graph where vertices are randomly placed in a 2D space
    and edges are formed between vertices that are within a certain distance 'r' of each other.

    Parameters:
        n (int): Number of vertices.
        r (float): Maximum edge length.

    Returns:
        tuple: Tuple containing the vertices and edges of the random graph.
    """
    # Generate random coordinates for vertices
    vertices = [(random.random(), random.random()) for _ in range(n)]
    edges = []
    # Check distances between vertices to form edges
    for i in range(n):
        for j in range(i + 1, n):
            if (vertices[i][0] - vertices[j][0]) ** 2 + (vertices[i][1] - vertices[j][1]) ** 2 <= r ** 2:
                edges.append((i, j))
                edges.append((j, i))
    return vertices, edges


def main():
    # Generate a graph with 10 vertices and maximum edge length of 0.7
    v, e = generate_geometric_graph(10, 0.7)

    with open('graph.edges', 'w') as f:
        # # Write vertices
        # for i, vertex in enumerate(v):
        #     f.write(f"v {i} {vertex[0]} {vertex[1]}\n")
        # Write edges
        for edge in e:
            f.write(f"{edge[0]} {edge[1]}\n")

if __name__ == '__main__':
    main()
