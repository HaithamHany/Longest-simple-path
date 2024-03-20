from Graph import Graph, Vertex
from typing import List
from math import sqrt
from random import choice


def DFS_CONNECTED_COMPONENTS(G: Graph) -> List[Vertex]:
    G.reset_vertices()  # Reset all vertices to the initial state
    G.time = 0
    largest_component = []
    for v in G.V:
        if v.color == "WHITE":
            component = []
            DFS_VISIT(G, v, component)
            if len(component) > len(largest_component):
                largest_component = component
    return largest_component


def DFS(G: Graph):
    G.reset_vertices()  # Reset all vertices to the initial state
    G.time = 0
    for v in G.V:
        if v.color == "WHITE":
            DFS_VISIT(G, v)


def DFS_VISIT(G: Graph, v: Vertex, component=None):
    G.time += 1
    v.d = G.time
    v.color = "GRAY"
    if component is not None:
        component.append(v)
    for u in G.Adj(v):
        if u.color == "WHITE":
            u.pi = v
            DFS_VISIT(G, u, component)
    G.time += 1
    v.f = G.time
    v.color = "BLACK"


def DFS_VISIT_RETURN_DEEPEST(G, start_vertex):
    G.reset_vertices()  # Reset all vertices to the initial state
    G.time = 0
    deepest_vertex = {'vertex': None, 'depth': -1}
    DFS_VISIT_VERTEX(G, start_vertex, deepest_vertex)
    return deepest_vertex['vertex']


def DFS_VISIT_VERTEX(G, u, deepest_vertex, current_depth=0):
    # Recursive DFS visit that tracks the deepest vertex
    G.time += 1
    u.d = G.time  # Discovery time
    u.color = 'GRAY'

    if current_depth > deepest_vertex['depth']:
        deepest_vertex['vertex'] = u
        deepest_vertex['depth'] = current_depth

    for v in G.Adj(u):
        if v.color == 'WHITE':
            print(current_depth)
            v.pi = u
            DFS_VISIT_VERTEX(G, v, deepest_vertex, current_depth + 1)

    G.time += 1
    u.f = G.time  # Finish time
    u.color = 'BLACK'


def DFS_BASED_LONGUEST_SIMPLE_PATH(G: Graph):
    LCC = DFS_CONNECTED_COMPONENTS(G)
    print(G)
    L_max = 0
    V_LCC = len(LCC)
    print(V_LCC)
    #for i in range(int(sqrt(V_LCC))):
    u = choice(LCC)
    v = DFS_VISIT_RETURN_DEEPEST(G, u)
    print(u,v)
    print(G)
    #w = DFS_VISIT_RETURN_DEEPEST(G, v)
    #L_max = max(L_max, v.d, w.d)
    return L_max


def main():
    file = "graph.edges"
    # file = "inf-euroroad.edges"
    G = Graph(file=file, verbose=0)
    # DFS(G)
    L_max = DFS_BASED_LONGUEST_SIMPLE_PATH(G)
    print(L_max)


if __name__ == "__main__":
    main()
