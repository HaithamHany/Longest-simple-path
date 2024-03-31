import random


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
        self.h = 0.0  # Heuristic distance

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
                f"d: {self.d} | f: {self.f} | x: {self.x} | y: {self.y} | h: {self.h} ")

    def reset(self):
        """
        Resets the vertex properties to their initial state.

        This method is typically used to prepare the vertex for another graph algorithm after it has been used.
        """
        self.color = 'WHITE'  # Reset color to 'WHITE'
        self.pi = None  # Remove predecessor
        self.d = 0  # Reset discovery time
        self.f = 0  # Reset finish time
        self.h = 0.0  # Reset distance heuristic

    def __lt__(self, other):
        """
        Compares two vertices based on their key value (u.d + u.h).

        Parameters:
            other (Vertex): The other vertex to compare against.

        Returns:
            bool: True if the current vertex has a smaller key value (u.d + u.h), False otherwise.
        """
        return (self.d + self.h) < (other.d + other.h)