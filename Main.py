from time import time
import sys
sys.setrecursionlimit(1500)
from DFS import DFS
from DijkstraMax import DijkstraMax
from GraphMetrics import GraphMetrics
from Heuristics import Heuristics
from Graph import Graph
import random
from Graph import Graph
from Heuristics import Heuristics as h
from math import sqrt


def binary_search(n, interval, filename: str):
    g = Graph()
    left, right = 0, sqrt(2)
    success = False

    while right - left > 1e-6:  # Binary search tolerance
        r = (left + right) / 2
        g.generate_random_geometric_graph_full(n, r, filename)
        dfs = DFS(graph=g)
        lcc = dfs.DFS_LCC()  # Returns the list of nodes in the LCC
        VLCC = len(lcc)

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


def create_random_graphs():
    conditions = [(300, [0.9, 0.95]), (400, [0.8, 0.9]), (500, [0.7, 0.8])]
    file_name = ["random_geometric_graph_OUTPUT_1.edges", "random_geometric_graph_OUTPUT_2.edges",
                 "random_geometric_graph_OUTPUT_3.edges"]
    for i, (n, interval) in enumerate(conditions):
        binary_search(n, interval, file_name[i])


def lsp_test(file: str = None):
    g = Graph()
    try:
        g.read_edges_with_coordinates_from_file(file) if file is not None else g.generate_random_geometric_graph_full(15,
                                                                                                                  0.5)
    except IndexError:
        g.read_edges_from_file(file)

    # LCC
    dfs = DFS(g)
    start_lcc = time()
    lcc = dfs.DFS_LCC()
    end_lcc = time()
    print("Largest Connected Component:", lcc)

    # DFS
    start_dfs = time()
    dfs_lsp_length, dfs_lsp_path = dfs.find_lsp()
    end_dfs = time()
    print("Longest Simple Path Length:", dfs_lsp_length)
    print("Longest Simple Path:", dfs_lsp_path)

    # Dijkstra
    # start_dijkstra = time()
    # d = DijkstraMax(g)
    # dijkstra_path, dijkstra_length = d.get_longest_path()
    # end_dijkstra = time()
    # print("The Longest Simple Path (LSP) is:", dijkstra_path, "with length:", dijkstra_length)

    # # A* and IDA*
    # h = Heuristics(g, lcc)
    #
    # start_astar = time()
    # s, d = lcc[0], lcc[-1]
    # astar_lsp_path = h.aStar_longest_path(s, d)
    # end_astar = time()
    # print("Longest Simple Path:", astar_lsp_path)
    #
    # start_ida_star = time()
    # start, goal = lcc[0], lcc[-1]
    # ida_path = h.ida_star_longest_path(start, goal)
    # end_ida_star = time()
    # print("IDA* Longest Simple Path:", ida_path)

    # Print table
    print("Heuristic\t\tTime (s)\tLongest Path")
    print("===============================================")
    print(f"LCC (DFS_LCC)\t{end_lcc - start_lcc:.6f}\t{len(lcc)} -> vertices count")
    print(f"DFS\t\t\t\t{end_dfs - start_dfs:.6f}\t{dfs_lsp_length} -> edges count")
    # print(f"Dijkstra's\t\t{end_dijkstra - start_dijkstra:.6f}\t{dijkstra_path} -> edges count")
    # print(f"A*\t\t\t\t{end_astar - start_astar:.6f}\t{len(astar_lsp_path)}")
    # print(f"IDA*\t\t\t{end_ida_star - start_ida_star:.6f}\t{len(ida_path)}")
    print("===============================================")

    # DFS Metrics
    dfs_metrics = GraphMetrics(g, lcc, dfs_lsp_path)
    dfs_metrics_results = dfs_metrics.print_all_metrics("DFS METRICS")
    print(dfs_metrics_results)

    print("===============================================")

    # # Dijkstra Metrics
    # dijkstra_metrics = GraphMetrics(g, lcc, dijkstra_length)
    # dijkstra_metrics_results = dijkstra_metrics.print_all_metrics("DIJKSTRA METRICS")
    # print(dijkstra_metrics_results)


if __name__ == "__main__":
    #create_random_graphs()  # Creating the graphs for the project requirements
    fileName = "Graphs/inf-power.mtx"  # Path to the graph file
    lsp_test(fileName)
