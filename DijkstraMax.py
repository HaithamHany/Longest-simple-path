import heapq


class PriorityQueueNode:
    def __init__(self, vertex):
        self.vertex = vertex

    def __lt__(self, other):
        return self.vertex.d > other.vertex.d  # Max heap based on d value


class DijkstraMax:
    def __init__(self, graph):
        self.graph = graph
        self.Q = []  # Priority queue

    def initialize_single_source_max(self, s):
        for v in self.graph.V:  # Use the list of vertices from the Graph class
            v.d = float('-inf')
            v.pi = None
            setattr(v, 'visited', False)  # Dynamically add 'visited' attribute
        s.d = 0
        setattr(s, 'visited', True)  # Dynamically mark as visited
        heapq.heappush(self.Q, PriorityQueueNode(s))  # Push wrapped vertex

    def relax_max(self, u, v):
        if v.d < u.d + 1:
            v.d = u.d + 1
            v.pi = u
            return True  # Indicates that v.d was increased
        return False

    def dijkstra_max(self, s):
        self.initialize_single_source_max(s)

        while self.Q:
            u = heapq.heappop(self.Q).vertex

            for v in self.graph.Adj(u):
                if self.relax_max(u, v) and not getattr(v, 'visited', False):
                    setattr(v, 'visited', True)
                    heapq.heappush(self.Q, PriorityQueueNode(v))

        # Return vertices sorted by their d value in descending order
        return sorted(self.graph.V, key=lambda x: x.d, reverse=True)