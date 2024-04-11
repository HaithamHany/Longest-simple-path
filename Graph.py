import random
from tqdm import tqdm

class Vertex:
    """
    A class representing a vertex in a graph.

    Attributes:
        id (any): The unique identifier of the vertex.
        color (str): The color of the vertex, used in graph algorithms to mark state. Initially 'WHITE'.
        d (int): Discovery time of the vertex in a graph traversal algorithm.
        f (int): Finish time of the vertex in a graph traversal algorithm.
        pi (Vertex): The predecessor vertex in a traversal path. None if the vertex has no predecessor.
        x (float): The x-coordinate of the vertex.
        y (float): The y-coordinate of the vertex.

    Methods:
        __init__(self, id): Initializes a new instance of the Vertex class.
        __eq__(self, other): Checks if another vertex is equal to the current instance based on the vertex id.
        __hash__(self): Returns a hash based on the vertex id.
        __str__(self): Returns a string representation of the vertex.
        reset(self): Resets the vertex properties to their initial state.
    """

    def __init__(self, id):
        """
        Initializes a new instance of the Vertex class.

        Parameters:
            id (any): The unique identifier of the vertex.
        """
        self.id = id
        self.color = 'WHITE'  # Initial color set to 'WHITE'
        self.d = 0  # Discovery time, initially 0
        self.f = 0  # Finish time, initially 0
        self.pi = None  # Predecessor, initially None
        self.x = random.random()  # Random x-coordinate between 0 and 1
        self.y = random.random()  # Random y-coordinate between 0 and 1

    def __eq__(self, other):
        """
        Checks if another vertex is equal to the current instance based on the vertex id.

        Parameters:
            other (Vertex): The other vertex to compare against.

        Returns:
            bool: True if the vertices are equal (same id), False otherwise.
        """
        eq = isinstance(other, Vertex) and self.id == other.id
        return eq

    def __hash__(self):
        """
        Returns a hash based on the vertex id.

        Returns:
            int: The hash of the vertex id.
        """
        return hash(self.id)

    def __str__(self):
        """
        Returns a string representation of the vertex.

        Returns:
            str: The string representation of the vertex.
        """
        predecessor_id = 'None' if self.pi is None else "Vertex " + str(self.pi.id)
        return (f"Vertex id: {self.id} | color: {self.color} | pi: {predecessor_id} | "
                f"d: {self.d} | f: {self.f} | x: {self.x} | y: {self.y}")

    def reset(self):
        """
        Resets the vertex properties to their initial state.

        This method is typically used to prepare the vertex for another graph algorithm after it has been used.
        """
        self.color = 'WHITE'  # Reset color to 'WHITE'
        self.pi = None  # Remove predecessor
        self.d = 0  # Reset discovery time
        self.f = 0  # Reset finish time

    def __lt__(self, other):
        """
        Compares two vertices based on their id.

        Parameters:
            other (Vertex): The other vertex to compare against.

        Returns:
            bool: True if the current vertex is less than the other vertex, False otherwise.
        """
        return self.id < other.id


class Edge:
    """
    Represents an undirected edge in a graph, connecting two vertices.

    Attributes:
        vertex_u: The first vertex of the edge.
        vertex_v: The second vertex of the edge.
    """

    def __init__(self, vertex_u, vertex_v):
        """
        Initializes an Edge instance with two vertices.

        Parameters:
            vertex_u: The first vertex of the edge.
            vertex_v: The second vertex of the edge.
        """
        self.vertex_u = vertex_u  # First endpoint of the edge
        self.vertex_v = vertex_v  # Second endpoint of the edge

    def __eq__(self, other):
        """
        Checks if this edge is equal to another edge. Two edges are considered equal if they connect the same pair of vertices,
        regardless of the order of the vertices.

        Parameters:
            other: The Edge instance to compare with.

        Returns:
            bool: True if the edges are equal, False otherwise.
        """
        eq = isinstance(other, Edge) and (
            (self.vertex_u == other.vertex_u and self.vertex_v == other.vertex_v) or
            (self.vertex_u == other.vertex_v and self.vertex_v == other.vertex_u)
        )
        return eq

    def __hash__(self):
        """
        Returns a hash that allows Edge to be used in sets or as dictionary keys.
        The hash is designed so that the order of vertices doesn't affect the hash value, making the edge "undirected" in nature.

        Returns:
            int: The hash of the edge.
        """
        # This ensures that the hash is the same regardless of the order of vertex_u and vertex_v
        return hash(frozenset([self.vertex_u, self.vertex_v]))

    def __str__(self):
        """
        Provides a string representation of the edge, showing the IDs of the vertices it connects.

        Returns:
            str: A string showing the connected vertices' IDs.
        """
        # Note: This assumes that the vertex objects have an 'id' attribute.
        s = f"Edge between: {self.vertex_u.id} <-> {self.vertex_v.id}"
        return s


class Graph:
    """
    Represents a graph structure loaded from a file. This graph supports operations like reading from a file,
    resetting vertices, finding adjacent vertices, and printing the graph's vertices and edges.

    Attributes:
        file (str): The path to the file from which the graph is read.
        verbose (int): Determines the verbosity of the string representation. If 1, edges are included.
    """

    def __init__(self, file, verbose=0):
        """
        Initializes the Graph instance by reading from the specified file.

        Parameters:
            file (str): The path to the file from which the graph is to be read.
            verbose (int, optional): Level of detail for string representation. Defaults to 0.

        Raises:
            ValueError: If the file path is not specified.
        """
        self.file = file
        self.time = 0  # Placeholder for potential future use, e.g., for graph algorithms that use timing
        self.verbose = verbose
        if file is not None:
            self._read_graph()  # Private method to read the graph structure from the file
        else:
            raise ValueError("File must be specified.")

    def _read_graph(self):
        """
        Private method to read the graph's vertices and edges from a file specified by `self.file`.
        """
        self.V, self.E = [], []  # Initialize lists for vertices (V) and edges (E)
        vertex_map = {}  # Map to track existing vertices by ID to ensure uniqueness
        with open(self.file, "r") as file:
            for l in tqdm(file.readlines()):
                line_split = l.split(" ")
                u_id, v_id = int(line_split[0]), int(line_split[1])

                # Reuse vertex if it exists, otherwise create a new one and add to map
                if u_id not in vertex_map:
                    u = Vertex(id=u_id)
                    vertex_map[u_id] = u
                    self.V.append(u)
                else:
                    u = vertex_map[u_id]

                if v_id not in vertex_map:
                    v = Vertex(id=v_id)
                    vertex_map[v_id] = v
                    self.V.append(v)
                else:
                    v = vertex_map[v_id]

                e = Edge(vertex_u=u, vertex_v=v)  # Create edge with the existing vertex instances
                if e not in self.E:
                    self.E.append(e)

    def reset_vertices(self):
        """
        Resets all vertices in the graph, assuming a reset method is defined for Vertex instances.
        Also resets vertices associated with each edge.
        """
        for v in self.V:
            v.reset()  # Assumes a reset method in Vertex
        for e in self.E:
            e.vertex_u.reset()
            e.vertex_v.reset()

    def Adj(self, v):
        """
        Finds all vertices adjacent to a given vertex.

        Parameters:
            v (Vertex): The vertex to find the adjacents for.

        Returns:
            list: A list of vertices adjacent to `v`.
        """
        Adj_v = []
        for e in self.E:
            if e.vertex_u == v:
                Adj_v.append(e.vertex_v)
            elif e.vertex_v == v:
                Adj_v.append(e.vertex_u)
        return Adj_v

    def __str__(self):
        """
        Provides a string representation of the graph, optionally including edges based on the verbose attribute.

        Returns:
            str: A string representation of the graph.
        """
        s = "-------- Graph Vertices --------\n"
        for v in self.V:
            s += str(v) + '\n'
        if self.verbose == 1:
            s += "-------- Graph Edges --------\n"
            for e in self.E:
                s += str(e) + '\n'
        return s

    def __contains__(self, n):
        """
        Checks if a vertex is part of the graph.

        Parameters:
            n (Vertex): The vertex to check.

        Returns:
            bool: True if `n` is in the graph's vertices, False otherwise.
        """
        return n in self.V

