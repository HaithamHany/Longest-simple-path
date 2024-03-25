from Vertex import Vertex
from Edge import Edge

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
        with open(self.file, "r") as file:
            f = file.readlines()
        for l in f:
            line_split = l.split(" ")
            u = Vertex(id=int(line_split[0]))  # Assumes existence of a Vertex class with an 'id' attribute
            v = Vertex(id=int(line_split[1]))
            e = Edge(vertex_u=u, vertex_v=v)  # Assumes existence of an Edge class
            if e not in self.E:
                self.E.append(e)
            if u not in self.V:
                self.V.append(u)
            if v not in self.V:
                self.V.append(v)

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
            v (Vertex): The vertex to find the adjacent for.

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

