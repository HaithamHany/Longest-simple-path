import os
from time import time
import sys
from DFS import DFS
from DijkstraMax import DijkstraMax
from Grasp import Grasp
from Spinner import Spinner
from aStar import aStar
from GraphMetrics import GraphMetrics
from Graph import Graph
from math import sqrt
import threading

sys.setrecursionlimit(1500)

spinner = Spinner()
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

    # Initialize the graph and read edges from file
    g = Graph()
    try:
        g.read_edges_with_coordinates_from_file(file) if file is not None else g.generate_random_geometric_graph_full(
            100,
            0.1)
    except IndexError:
        g.read_edges_from_file(file)

    # LCC (DFS_LCC)
    dfs = DFS(g)
    start_lcc = time()
    lcc = dfs.DFS_LCC()
    end_lcc = time()
    print("Largest Connected Component:", lcc)


    spinner.start()

    # DijkstraMax
    dijkstra = DijkstraMax(g, lcc)
    start_dijkstra = time()
    dijkstra_length, dijkstra_path = dijkstra.get_longest_path()
    end_dijkstra = time()
    print("Dijkstra's Longest Simple Path Length:", dijkstra_length)
    print("Dijkstra's Longest Simple Path:", dijkstra_path)

    # DFS
    start_dfs = time()
    dfs_lsp_length, dfs_lsp_path = dfs.find_lsp()
    end_dfs = time()
    print("DFS Longest Simple Path Length:", dfs_lsp_length)
    print("DFS Longest Simple Path:", dfs_lsp_path)

    # A*
    astar = aStar(g, lcc)
    start_astar = time()
    astar_length, astar_lsp_path = astar.find_longest_simple_path()
    end_astar = time()
    print("A* Longest Simple Path Length:", len(astar_lsp_path))
    print("A* Longest Simple Path:", astar_lsp_path)

    # GRASP
    grasp = Grasp(g, lcc)
    start_grasp = time()
    grasp_lsp_path = grasp.grasp_longest_path()
    end_grasp = time()
    print("GRASP Longest Simple Path Length:", len(grasp_lsp_path))
    print("GRASP Longest Simple Path:", grasp_lsp_path)

    # Print the table with results
    print("\nHeuristic\t\tTime (s)\tLongest Path Length")
    print("===============================================")
    print(f"LCC (DFS_LCC)\t{end_lcc - start_lcc:.6f}\t{len(lcc)} -> vertices count")
    print(f"Dijkstra's\t\t{end_dijkstra - start_dijkstra:.6f}\t{dijkstra_length} -> edges count")
    print(f"DFS\t\t\t\t{end_dfs - start_dfs:.6f}\t{dfs_lsp_length} -> edges count")
    print(f"A*\t\t\t\t{end_astar - start_astar:.6f}\t{len(astar_lsp_path)} -> vertices count")
    print(f"GRASP\t\t\t{end_grasp - start_grasp:.6f}\t{len(grasp_lsp_path)} -> vertices count")
    print("===============================================")

    # Calculate and print metrics for each method
    print("\nMetrics:")
    print("===============================================")
    # Metrics for LCC (DFS_LCC)
    lcc_metrics = GraphMetrics(g, lcc, [])
    lcc_metrics_results = lcc_metrics.print_all_metrics("LCC Metrics")
    print(lcc_metrics_results)
    print("===============================================")
    # Metrics for DijkstraMax
    dijkstra_metrics = GraphMetrics(g, lcc, dijkstra_path)
    dijkstra_metrics_results = dijkstra_metrics.print_all_metrics("DijkstraMax Metrics")
    print(dijkstra_metrics_results)
    print("===============================================")
    # Metrics for DFS
    dfs_metrics = GraphMetrics(g, lcc, dfs_lsp_path)
    dfs_metrics_results = dfs_metrics.print_all_metrics("DFS Metrics")
    # print(dfs_metrics_results)
    print("===============================================")
    # Metrics for A*
    astar_metrics = GraphMetrics(g, lcc, astar_lsp_path)
    astar_metrics_results = astar_metrics.print_all_metrics("A* Metrics")
    print(astar_metrics_results)
    print("===============================================")
    # Metrics for GRASP
    grasp_metrics = GraphMetrics(g, lcc, grasp_lsp_path)
    grasp_metrics_results = grasp_metrics.print_all_metrics("GRASP Metrics")
    print(grasp_metrics_results)
    spinner.stop()


def list_files(directory):
    """List all files in a directory."""
    return [f for f in os.listdir(directory) if os.path.isfile(os.path.join(directory, f))]


def select_file():
    directory = "Graphs"  # Set your directory
    files = list_files(directory)

    if not files:
        print("No files found.")
        return None

    print("Available files:")
    for index, file in enumerate(files):
        print(f"{index + 1}: {file}")

    while True:
        try:
            selection = int(input("Select a file by number: ")) - 1
            if 0 <= selection < len(files):
                return files[selection]
            else:
                print("Invalid selection. Please try again.")
        except ValueError:
            print("Invalid input. Please enter a number.")


if __name__ == "__main__":
    while True:
        spinner.stop()
        print("===============================================")
        file_name = select_file()
        if file_name is None:
            break
        file_path = f"Graphs/{file_name}"
        lsp_test(file_path)
