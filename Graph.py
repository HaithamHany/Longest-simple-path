class Vertex:
    def __init__(self, id):
        self.id = id
        self.color = 'WHITE'
        self.d = 0  # Discovery time
        self.f = 0  # Finish time
        self.pi = None  # Predecessor

    def __eq__(self, other):
        return isinstance(other, Vertex) and self.id == other.id

    def __hash__(self):
        return hash(self.id)

    def __str__(self):
        predecessor_id = 'None' if self.pi is None else "Vertex " + str(self.pi.id)
        return (f"Vertex id: {self.id} | color: {self.color} | pi: {predecessor_id} | "
                f"d: {self.d} | f: {self.f}")

    def reset(self):
        self.color = 'WHITE'
        self.pi = None
        self.d = 0
        self.f = 0


class Edge:
    def __init__(self, vertex_u, vertex_v):
        self.vertex_u = vertex_u
        self.vertex_v = vertex_v

    def __eq__(self, other):
        return isinstance(other, Edge) and (
            (self.vertex_u == other.vertex_u and self.vertex_v == other.vertex_v) or
            (self.vertex_u == other.vertex_v and self.vertex_v == other.vertex_u)
        )

    def __str__(self):
        s = f"Edge between: {self.vertex_u.id} <-> {self.vertex_v.id}"
        return s


class Graph:
    def __init__(self, file, verbose=0):
        self.file = file
        self.time = 0
        self.verbose = verbose
        if file is not None:
            self._read_graph()
        else:
            raise ValueError("If the file is not specified y")

    def _read_graph(self):
        self.V, self.E = [], []
        with open(self.file, "r") as file:
            f = file.readlines()
        for l in f:
            line_split = l.split(" ")
            u = Vertex(id=int(line_split[0]))
            v = Vertex(id=int(line_split[1]))
            e = Edge(vertex_u=u, vertex_v=v)
            if e not in self.E:
                self.E.append(e)
            if u not in self.V:
                self.V.append(u)
            if v not in self.V:
                self.V.append(v)

    def reset_vertices(self):
        for v in self.V:
            v.reset()

    def Adj(self, v):
        Adj_v = []
        for e in self.E:
            if e.vertex_u == v:
                Adj_v.append(e.vertex_v)
        return Adj_v

    def __str__(self):
        s = ""
        s += "-------- Graph Vertices --------\n"
        for v in self.V:
            s += v.__str__() + '\n'
        if self.verbose == 1:
            s += "-------- Graph Edges --------\n"
            for e in self.E:
                s += e.__str__() + '\n'
        return s

    def __contains__(self, n):
        return n in self.V

