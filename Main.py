from time import time

from DFS import DFS
from DijkstraMax import DijkstraMax
from Heuristics import Heuristics
from Graph import Graph


def lsp_test(file: str):
    g = Graph()
    g.read_edges_from_file(file)

    #LCC
    dfs = DFS(g)
    start_lcc = time()
    lcc = dfs.DFS_LCC()
    end_lcc = time()
    print("Largest Connected Component:", lcc)

    #DFS
    start_dfs = time()
    lsp_length, lsp_path = dfs.find_lsp()
    end_dfs = time()
    print("Longest Simple Path Length:", lsp_length)
    print("Longest Simple Path:", lsp_path)

    #Dijkstra
    start_dijkstra = time()
    d = DijkstraMax(g)
    path, length = d.get_longest_path()
    end_dijkstra = time()
    print("The Longest Simple Path (LSP) is:", path, "with length:", length)

    #A* and IDA*
    h = Heuristics(g, lcc)

    start_astar = time()
    s, d = lcc[0], lcc[-1]
    astar_lsp_path = h.aStar_longest_path(s, d)
    end_astar = time()
    print("Longest Simple Path:", astar_lsp_path)

    start_ida_star = time()
    start, goal = lcc[0], lcc[-1]
    ida_path = h.ida_star_longest_path(start, goal)
    end_ida_star = time()
    print("IDA* Longest Simple Path:", ida_path)


    # Print table
    print("Heuristic\t\tTime (s)\tLongest Path")
    print("===============================================")
    print(f"LCC (DFS_LCC)\t{end_lcc - start_lcc:.6f}\t{len(lcc)} -> vertices count")
    print(f"DFS\t\t\t\t{end_dfs - start_dfs:.6f}\t{lsp_length} -> edges count")
    print(f"Dijkstra's\t\t{end_dijkstra - start_dijkstra:.6f}\t{path} -> edges count")
    print(f"A*\t\t\t\t{end_astar - start_astar:.6f}\t{len(astar_lsp_path)}")
    print(f"IDA*\t\t\t{end_ida_star - start_ida_star:.6f}\t{len(ida_path)}")


if __name__ == "__main__":
    fileName = "graph.edges.txt"  # Path to the graph file
    lsp_test(fileName)
