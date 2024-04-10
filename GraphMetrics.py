class GraphMetrics:
    def __init__(self, graph, lcc, lsp):
        # Initialize the metrics calculator with the graph, its largest connected component, and the longest simple path.
        self.graph = graph
        self.lcc = lcc
        self.lsp = lsp

    def number_of_nodes(self):
        # Return the number of nodes in the graph.
        return len(self.graph.nodes)

    def lcc_size(self):
        # Return the number of nodes in the largest connected component.
        return len(self.lcc)

    def max_degree(self):
        # Return the maximum degree of any node in the largest connected component.
        return max(self.graph.degree(node) for node in self.lcc)

    def average_degree(self):
        # Return the average degree of nodes in the largest connected component.
        return sum(self.graph.degree(node) for node in self.lcc) / len(self.lcc)

    def lsp_length(self):
        # Return the length of the longest simple path found in the LCC.
        return len(self.lsp) - 1

    def calculate_all_metrics(self):
        # Return the length of the longest simple path found in the LCC.
        return {
            'n': self.number_of_nodes(),
            '|VLCC|': self.lcc_size(),
            '∆(LCC)': self.max_degree(),
            'k(LCC)': self.average_degree(),
            'Lmax': self.lsp_length(),
        }
