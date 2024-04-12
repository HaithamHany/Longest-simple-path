class PriorityQueueNode:
    def __init__(self, vertex, distance):
        self.vertex = vertex
        self.distance = distance

    def __lt__(self, other):
        return self.distance > other.distance