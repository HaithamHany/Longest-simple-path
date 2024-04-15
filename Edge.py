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

    def __str__(self):
        """
        Provides a string representation of the edge, showing the IDs of the vertices it connects.

        Returns:
            str: A string showing the connected vertices' IDs.
        """
        # Note: This assumes that the vertex objects have an 'id' attribute.
        s = f"Edge between: {self.vertex_u.id} <-> {self.vertex_v.id}"
        return s