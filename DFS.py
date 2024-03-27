from Graph import Graph, Vertex
from typing import List
from math import sqrt
from random import choice
import sys
from time import time
sys.setrecursionlimit(2000) # important because for large graph we will need lost of recursion for DFS


def DFS_LCC(G: Graph) -> List[Vertex]:
    """
    Finds the largest connected component (LCC) in a graph using depth-first search (DFS).

    This function iterates over all vertices in the graph, performing DFS starting from each
    unvisited (color == "WHITE") vertex. It tracks the vertices visited during each DFS
    as a component and updates the largest component found throughout the process.

    Parameters:
        G (Graph): The graph on which to perform DFS to find the LCC.

    Returns:
        List[Vertex]: A list of vertices belonging to the largest connected component.
    """
    G.reset_vertices()  # Reset all vertices to the initial state, typically setting their color to "WHITE"
    G.time = 0  # Time counter used in DFS_VISIT, might track discovery/finish times of vertices

    largest_component = []  # Initialize empty list to store the vertices of the largest component found
    for v in G.V:  # Iterate over each vertex in the graph
        if v.color == "WHITE":  # Check if the vertex has not been visited
            component = []  # Initialize list to store vertices of the current component
            DFS_VISIT(G, v, component)  # Perform DFS starting from the current vertex, filling 'component'
            if len(component) > len(
                    largest_component):  # If the current component is larger than the largest found so far
                largest_component = component  # Update the largest component

    return largest_component  # Return the vertices of the largest connected component


def DFS(G: Graph):
    """
    Performs a depth-first search (DFS) on the entire graph G. This function iterates over all vertices
    in the graph and initiates a DFS from each unvisited (white-colored) vertex. This is typically used
    to explore the graph fully, for purposes like graph traversal, finding connected components, or
    other graph algorithms that require visiting all vertices.

    Parameters:
        G (Graph): The graph on which to perform the DFS. It is assumed that the Graph class
                   has a method `reset_vertices` to initialize vertex states, and an iterable
                   collection of vertices `V` with a `color` attribute used to mark their visitation status.
    """
    G.reset_vertices()  # Reset all vertices to their initial state, typically setting their color to "WHITE"
    G.time = 0  # Initialize a time counter used by DFS_VISIT, may track discovery/finishing times of vertices

    for v in G.V:  # Iterate over each vertex in the graph
        if v.color == "WHITE":  # If the vertex is unvisited
            DFS_VISIT(G, v)  # Perform a depth-first search from the vertex


def DFS_VISIT(G: Graph, v: Vertex, component=None):
    """
    Perform a depth-first search visit starting from vertex v in graph G.
    This function marks the discovery and finishing times for each vertex
    and categorizes vertices into different connected components if the component
    parameter is provided. It also assigns colors to vertices to track the progress:
    WHITE for unvisited vertices, GRAY for vertices being visited, and BLACK for visited vertices.

    Parameters:
    - G (Graph): The graph on which DFS is being performed. The graph should have an attribute 'time'
      to keep track of the discovery and finishing times, and a method Adj(v) to get the adjacency list of vertex v.
    - v (Vertex): The current vertex being visited. The vertex should have attributes for discovery time 'd',
      finishing time 'f', color 'color', and predecessor 'pi'.
    - component (list, optional): A list to store the vertices of the same connected component. If provided,
      vertices will be added to this list as they are visited. Useful for finding connected components in a graph.

    Returns:
    None
    """
    # Increment the global time at the beginning of the visit
    G.time += 1
    v.d = G.time  # Set the discovery time of the vertex
    v.color = "GRAY"  # Mark the vertex as being visited

    # If a component list is provided, append the current vertex to it
    if component is not None:
        component.append(v)

    # Explore each adjacent vertex
    for u in G.Adj(v):
        if u.color == "WHITE":
            # If the vertex is unvisited
            u.pi = v  # Set the current vertex as the predecessor

            DFS_VISIT(G, u, component)  # Recursively visit the adjacent vertex

    # After exploring all adjacent vertices, increment the global time again
    G.time += 1
    v.f = G.time  # Set the finishing time of the vertex
    v.color = "BLACK"  # Mark the vertex as fully visited


def DFS_VISIT_RETURN_DEEPEST(G: Graph, start_vertex: Vertex) -> Vertex:
    """
    Perform a modified depth-first search (DFS) starting from a given vertex, aimed at finding
    the deepest vertex reachable from the start vertex. This function assumes that the graph
    has a method to reset the state of all vertices to their initial state (usually unvisited),
    and a method Adj(vertex) to get the adjacency list of a given vertex.

    Parameters:
    - G (Graph): The graph on which DFS is being performed. The graph should have a method `reset_vertices`
      to reset the state of all vertices, and a method Adj(v) to get the adjacency list of vertex v.
    - start_vertex (Vertex): The vertex from which the DFS starts.

    Returns:
    Vertex: The deepest vertex reached during the DFS. If multiple vertices are at the same depth,
    the function returns the first one encountered at this maximum depth.

    Note:
    This function uses a helper function DFS_VISIT_VERTEX (not defined here) to perform the recursive
    DFS. This helper function should update the 'deepest_vertex' dictionary with the deepest vertex found
    and its depth, and it likely tracks the current depth as it recurses through the graph.
    """
    G.reset_vertices()  # Reset all vertices to their initial state, typically marking them as unvisited
    G.time = 0  # Reset the global time counter
    deepest_vertex = {'vertex': None, 'depth': -1}  # Initialize the record for the deepest vertex found
    # Start the DFS from the start_vertex, passing the current depth (0) and the record for tracking the deepest vertex
    DFS_VISIT_VERTEX(G, start_vertex, deepest_vertex, 0)
    # After the DFS, return the vertex that was found to be the deepest
    return deepest_vertex['vertex']


def DFS_VISIT_VERTEX(G, u, deepest_vertex, current_depth=0):
    """
    Perform a recursive depth-first search (DFS) visit starting from a specific vertex, tracking the deepest vertex reached.

    This function updates discovery and finish times for each vertex, marks vertices with their current color status
    (GRAY for discovered, BLACK for finished), and keeps track of the deepest vertex reached in terms of the depth from
    the starting vertex.

    Parameters:
    - G: A graph object. This graph must have an attribute 'time' for global timestamp, a method Adj(u) that returns
    adjacent vertices to u, and vertices that have 'd' (discovery time), 'f' (finish time), 'color', and 'pi'
    (predecessor) attributes.
    - u: The current vertex being visited.
    - deepest_vertex: A dictionary that tracks the deepest vertex encountered during the DFS. It should have 'vertex'
     and 'depth' keys. 'vertex' holds the vertex object, and 'depth' represents its depth from the starting vertex.
    - current_depth (int, optional): The current depth of the DFS from the starting vertex. Defaults to 0.

    Returns:
    None. The function updates the graph G, the current vertex u, and the deepest_vertex dictionary in-place.
    """

    # Increment global time for discovery
    G.time += 1
    u.d = G.time  # Set the discovery time of the current vertex
    u.color = 'GRAY'  # Mark the current vertex as discovered but not finished
    # Update the deepest_vertex dictionary if the current depth is greater than the previously recorded deepest depth
    if current_depth > deepest_vertex['depth']:
        deepest_vertex['vertex'] = u
        deepest_vertex['depth'] = current_depth
    # Explore adjacent vertices
    for v in G.Adj(u):
        if v.color == 'WHITE':  # If the vertex has not been discovered
            v.pi = u  # Set the current vertex as the predecessor of v
            DFS_VISIT_VERTEX(G, v, deepest_vertex, current_depth + 1)  # Recursively visit v
    # After exploring all adjacent vertices, increment global time for finish and mark the vertex as finished
    G.time += 1
    u.f = G.time  # Set the finish time of the current vertex
    u.color = 'BLACK'  # Mark the current vertex as finished


def DFS_BASED_LONGEST_SIMPLE_PATH(G: Graph) -> int:
    """
    Finds the length of the longest simple path in a graph using a depth-first search (DFS) based heuristic.
    This function employs a heuristic approach that iteratively picks random vertices from the largest connected
    component (LCC) of the graph, then performs DFS from these vertices to find the deepest reachable vertex.
    By evaluating the distances from the initial vertex to the deepest vertex and the distance from this deepest vertex
    to its deepest reachable vertex, the function estimates the longest simple path length in the graph.

    Note: This function assumes the input graph is undirected and connected. If the graph is not connected,
    the function operates on its largest connected component (LCC).
    Parameters:
    - G: A graph object of type Graph. The graph should support the operations required by the `DFS_LCC` and
    `DFS_VISIT_RETURN_DEEPEST` functions.

    Returns:
    - L_max (int): An estimate of the length of the longest simple path in the graph.

    The actual implementation of `DFS_LCC` (to find the largest connected component) and `DFS_VISIT_RETURN_DEEPEST`
    (to perform a DFS visit and return the deepest vertex) are not shown. These functions must be implemented separately
    and should adhere to the Graph interface expected by this function.
    """

    # Find the largest connected component (LCC) of the graph
    LCC = DFS_LCC(G)
    # Initialize the maximum length of the simple path found
    L_max = 0
    # Calculate the number of vertices in the LCC
    V_LCC = len(LCC)
    # Perform the heuristic search sqrt(V_LCC) times to find the longest simple path
    for i in range(int(sqrt(V_LCC))):
        # Randomly choose a vertex from the LCC
        u = choice(LCC)
        # Perform DFS from the chosen vertex to find the deepest vertex from u
        v = DFS_VISIT_RETURN_DEEPEST(G, u)
        # Perform DFS from vertex v (found to be deep from u) to find the deepest vertex from v
        w = DFS_VISIT_RETURN_DEEPEST(G, v)
        # Update the maximum length found so far with the maximum of the current maximum,
        # the depth of v, and the depth of w
        L_max = max(L_max, v.d, w.d)
    # Return the maximum length of the simple path found
    return L_max


def main_heuristic_1(file: str):
    G = Graph(file=file, verbose=0)
    start = time()
    L_max = DFS_BASED_LONGEST_SIMPLE_PATH(G)
    end = time()
    print(f"Total time for first Heuristic: is {end - start:.3f}s, and the longest path for {file.split('.')[0]} "
          f"is {L_max}")


if __name__ == "__main__":
    #file = "graph.edges" # our graph
    file = "inf-euroroad.edges"
    main_heuristic_1(file)
