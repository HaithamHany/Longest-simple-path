import heapq
from Graph import Graph, Vertex
from typing import List
from math import sqrt
from random import choice
import sys
from time import time
sys.setrecursionlimit(1500)  # important because for large graph we will need lost of recursion for DFS


class PriorityQueueNode:
    def __init__(self, vertex, distance):
        self.vertex = vertex
        self.distance = distance  # Store the distance for comparison in the priority queue

    def __lt__(self, other):
        # Reverse the comparison to make it a max heap based on distance
        return self.distance > other.distance


class Heuristics:
    def __init__(self, graph):
        self.time = None
        self.graph = graph
        self.Q = []  # Priority queue

    def initialize_single_source_max(self, s):
        for v in self.graph.V:
            v.d = float('-inf')
            v.pi = None
        s.d = 0
        # Initialize the priority queue with all vertices, but start with s having distance 0
        for v in self.graph.V:
            heapq.heappush(self.Q, PriorityQueueNode(v, v.d))

    def relax_max(self, u, v):
        # Check if the new path to v through u is longer than the current known path to v
        if v.d < u.d + 1:
            v.d = u.d + 1
            v.pi = u
            return True
        return False

    def dijkstra_max(self, s):
        self.initialize_single_source_max(s)
        visited = set()

        while self.Q:
            u = heapq.heappop(self.Q).vertex
            if u in visited:
                continue
            visited.add(u)

            for v in self.graph.Adj(u):
                if self.relax_max(u, v):
                    # Instead of pushing new nodes to the queue, we update the distances
                    # and rely on the visited set to avoid processing a node more than once
                    heapq.heappush(self.Q, PriorityQueueNode(v, v.d))

        # Find the vertex with the maximum distance
        max_vertex = max((v for v in self.graph.V if v.d != float('-inf')), key=lambda x: x.d)

        # Calculate the number of edges in the longest path
        L_max_dijkstra = max_vertex.d - 1 if max_vertex.pi is not None else 0
        return L_max_dijkstra

    def DFS_LCC(self) -> List[Vertex]:
        """
        Finds the largest connected component (LCC) in a graph using depth-first search (DFS).

        This function iterates over all vertices in the graph, performing DFS starting from each
        unvisited (color == "WHITE") vertex. It tracks the vertices visited during each DFS
        as a component and updates the largest component found throughout the process.

        Returns:
            List[Vertex]: A list of vertices belonging to the largest connected component.
        """
        self.graph.reset_vertices()  # Reset all vertices to the initial state, typically setting their color to "WHITE"
        self.time = 0  # Time counter used in DFS_VISIT, might track discovery/finish times of vertices

        largest_component = []  # Initialize empty list to store the vertices of the largest component found
        for v in self.graph.V:  # Iterate over each vertex in the graph
            if v.color == "WHITE":  # Check if the vertex has not been visited
                component = []  # Initialize list to store vertices of the current component
                self.DFS_VISIT(v, component)  # Perform DFS starting from the current vertex, filling 'component'
                if len(component) > len(
                        largest_component):  # If the current component is larger than the largest found so far
                    largest_component = component  # Update the largest component

        return largest_component  # Return the vertices of the largest connected component

    def DFS(self):
        """
        Performs a depth-first search (DFS) on the entire graph G. This function iterates over all vertices
        in the graph and initiates a DFS from each unvisited (white-colored) vertex. This is typically used
        to explore the graph fully, for purposes like graph traversal, finding connected components, or
        other graph algorithms that require visiting all vertices.
        """
        self.graph.reset_vertices()  # Reset all vertices to their initial state, typically setting their color to "WHITE"
        self.time = 0  # Initialize a time counter used by DFS_VISIT, may track discovery/finishing times of vertices

        for v in self.graph.V:  # Iterate over each vertex in the graph
            if v.color == "WHITE":  # If the vertex is unvisited
                self.DFS_VISIT(v)  # Perform a depth-first search from the vertex

    def DFS_VISIT(self, v: Vertex, component=None):
        """
        Perform a depth-first search visit starting from vertex v in graph G.
        This function marks the discovery and finishing times for each vertex
        and categorizes vertices into different connected components if the component
        parameter is provided. It also assigns colors to vertices to track the progress:
        WHITE for unvisited vertices, GRAY for vertices being visited, and BLACK for visited vertices.

        Parameters:
        - v (Vertex): The current vertex being visited. The vertex should have attributes for discovery time 'd',
          finishing time 'f', color 'color', and predecessor 'pi'.
        - component (list, optional): A list to store the vertices of the same connected component. If provided,
          vertices will be added to this list as they are visited. Useful for finding connected components in a graph.
        """
        # Increment the global time at the beginning of the visit
        self.time += 1
        v.d = self.time  # Set the discovery time of the vertex
        v.color = "GRAY"  # Mark the vertex as being visited

        # If a component list is provided, append the current vertex to it
        if component is not None:
            component.append(v)

        # Explore each adjacent vertex
        for u in self.graph.Adj(v):
            if u.color == "WHITE":
                # If the vertex is unvisited
                u.pi = v  # Set the current vertex as the predecessor

                self.DFS_VISIT(u, component)  # Recursively visit the adjacent vertex

        # After exploring all adjacent vertices, increment the global time again
        self.time += 1
        v.f = self.time  # Set the finishing time of the vertex
        v.color = "BLACK"  # Mark the vertex as fully visited

    def DFS_VISIT_RETURN_DEEPEST(self, start_vertex: Vertex) -> Vertex:
        """
        Perform a modified depth-first search (DFS) starting from a given vertex, aimed at finding
        the deepest vertex reachable from the start vertex.

        Parameters:
        - start_vertex (Vertex): The vertex from which the DFS starts.

        Returns:
        Vertex: The deepest vertex reached during the DFS.
        """
        self.graph.reset_vertices()  # Reset all vertices to their initial state, typically marking them as unvisited
        self.time = 0  # Reset the global time counter
        deepest_vertex = {'vertex': None, 'depth': -1}  # Initialize the record for the deepest vertex found
        # Start the DFS from the start_vertex, passing the current depth (0) and the record for tracking the deepest vertex
        self.DFS_VISIT_VERTEX(start_vertex, deepest_vertex, 0)
        # After the DFS, return the vertex that was found to be the deepest
        return deepest_vertex['vertex']

    def DFS_VISIT_VERTEX(self, u, deepest_vertex, current_depth=0):
        """
        Perform a recursive depth-first search (DFS) visit starting from a specific vertex, tracking the deepest vertex reached.

        Parameters:
        - u: The current vertex being visited.
        - deepest_vertex: A dictionary that tracks the deepest vertex encountered during the DFS. It should have 'vertex'
         and 'depth' keys. 'vertex' holds the vertex object, and 'depth' represents its depth from the starting vertex.
        - current_depth (int, optional): The current depth of the DFS from the starting vertex. Defaults to 0.
        """
        # Increment global time for discovery
        self.time += 1
        u.d = self.time  # Set the discovery time of the current vertex
        u.color = 'GRAY'  # Mark the current vertex as discovered but not finished
        # Update the deepest_vertex dictionary if the current depth is greater than the previously recorded deepest depth
        if current_depth > deepest_vertex['depth']:
            deepest_vertex['vertex'] = u
            deepest_vertex['depth'] = current_depth
        # Explore adjacent vertices
        for v in self.graph.Adj(u):
            if v.color == 'WHITE':  # If the vertex has not been discovered
                v.pi = u  # Set the current vertex as the predecessor of v
                self.DFS_VISIT_VERTEX(v, deepest_vertex, current_depth + 1)  # Recursively visit v
        # After exploring all adjacent vertices, increment global time for finish and mark the vertex as finished
        self.time += 1
        u.f = self.time  # Set the finish time of the current vertex
        u.color = 'BLACK'  # Mark the current vertex as finished

    def DFS_BASED_LONGEST_SIMPLE_PATH(self) -> int:
        """
        Finds the length of the longest simple path in a graph using a depth-first search (DFS) based heuristic.

        Returns:
            int: An estimate of the length of the longest simple path in the graph.
        """
        # Find the largest connected component (LCC) of the graph
        LCC = self.DFS_LCC()
        # Initialize the maximum length of the simple path found
        L_max = 0
        # Calculate the number of vertices in the LCC
        V_LCC = len(LCC)
        # Perform the heuristic search sqrt(V_LCC) times to find the longest simple path
        for i in range(int(sqrt(V_LCC))):
            # Randomly choose a vertex from the LCC
            u = choice(LCC)
            # Perform DFS from the chosen vertex to find the deepest vertex from u
            v = self.DFS_VISIT_RETURN_DEEPEST(u)
            # Perform DFS from vertex v (found to be deep from u) to find the deepest vertex from v
            w = self.DFS_VISIT_RETURN_DEEPEST(v)
            # Update the maximum length found so far with the maximum of the current maximum,
            # the depth of v, and the depth of w
            L_max = max(L_max, v.d, w.d)
        # Return the maximum length of the simple path found
        return L_max

    def aStar(self, s, d):
        """
        A* algorithm to find the shortest path from source node s to destination node d in the graph.

        Parameters:
            s (Vertex): The source node.
            d (Vertex): The destination node.

        Returns:
            list: The shortest path from s to d.
        """
        self.initialize_single_source_max(s)
        for v in self.graph.V:
            # Set the heuristic distance from v to d
            v.h = ((d.x - v.x) ** 2 + (d.y - v.y) ** 2) ** 0.5  # Euclidean distance heuristic

        S = set()  # Closed list
        Q = []  # Max heap

        for u in self.graph.V:
            # The key value for node u in the max heap is u.d + u.h
            heapq.heappush(Q, (-1 * (u.d + u.h), u))

        while Q:
            _, u = heapq.heappop(Q)
            S.add(u)

            if u == d:
                break

            for v in self.graph.Adj(u):
                if self.relax_max(u, v):
                    priority = (-1 * (v.d + v.h), id(v))  # Add id(v) to break ties
                    if v in S:
                        S.remove(v)
                        heapq.heappush(Q, priority)
                    else:
                        heapq.heappush(Q, priority)

        return sorted(self.graph.V, key=lambda x: x.d, reverse=True)

    def euclidean_distance(self, v1, v2):

       #The Euclidean distance between v1 and v2.
        return sqrt((v1.x - v2.x) ** 2 + (v1.y - v2.y) ** 2)

    def ida_star(self, root, goal):
        def search(path, g, bound):
            node = path[-1]
            f = g + self.euclidean_distance(node, goal)
            if f > bound:
                return f, False
            if node == goal:
                return f, True
            min_bound = float('inf')
            found = False
            for neighbor in self.graph.Adj(node):
                if neighbor not in path:
                    path.append(neighbor)
                    t, found_path = search(path, g + 1, bound)  # Increment g since graph is unweighted
                    if found_path:
                        found = True
                        break  # Stop searching when the goal is found
                    if t < min_bound:
                        min_bound = t
                    path.pop()
            return min_bound, found

        bound = self.euclidean_distance(root, goal)
        path = [root]
        while True:
            t, found = search(path, 0, bound)
            if found:  # Path found
                return path
            if t == float('inf'):  # No solution
                return None
            bound = t  # Update the bound



def main_heuristic_1(file: str):
    # Initialize Heuristics object with the graph file
    heuristics = Heuristics(Graph(file=file, verbose=0))

    # Calculate LCC using DFS_LCC
    start_lcc = time()
    LCC = heuristics.DFS_LCC()
    end_lcc = time()

    # Calculate the longest path using DFS_BASED_LONGEST_SIMPLE_PATH
    start_dfs = time()
    L_max_dfs = heuristics.DFS_BASED_LONGEST_SIMPLE_PATH()
    end_dfs = time()

    # # Calculate the longest path using Dijkstra's algorithm
    # start_dijkstra = time()
    # L_max_dijkstra = heuristics.dijkstra_max(heuristics.graph.V[0])
    # end_dijkstra = time()
    #
    # # Calculate the longest path using A* algorithm
    # start_astar = time()
    # longest_path_astar = heuristics.aStar(heuristics.graph.V[0], heuristics.graph.V[-1])
    # L_max_astar = len(longest_path_astar) - 1  # Length of the path is one less than the number of vertices
    # end_astar = time()
    #
    # start_ida_star = time()
    # path_ida_star = heuristics.ida_star(heuristics.graph.V[0], heuristics.graph.V[-1])
    # L_maxIDAstar = len(path_ida_star) - 1 if path_ida_star else 0
    # end_ida_star = time()

    # Print table
    print("Heuristic\t\tTime (s)\tLongest Path")
    print("===============================================")
    print(f"LCC (DFS_LCC)\t{end_lcc - start_lcc:.6f}\t{len(LCC)}")
    print(f"DFS\t\t\t\t{end_dfs - start_dfs:.6f}\t{L_max_dfs}")
    # print(f"Dijkstra's\t\t{end_dijkstra - start_dijkstra:.6f}\t{L_max_dijkstra}")
    # print(f"A*\t\t\t\t{end_astar - start_astar:.6f}\t{L_max_astar}")
    # print(f"IDA*\t\t\t{end_ida_star - start_ida_star:.6f}\t{L_maxIDAstar}")


if __name__ == "__main__":
    fileName = "simple_graph_2.edges"  # Path to the graph file
    main_heuristic_1(fileName)

# For DFS and inf-power file, we have DFS (longuest path): 5982 and LCC: 4941
