class GraphMetrics:
    def __init__(self, graph, lcc, lsp):
        # graph is an instance of your Graph class
        # lcc is a list of nodes representing the largest connected component
        # lsp is a list of nodes representing the longest simple path
        self.graph = graph
        self.lcc = lcc
        self.lsp = lsp

    def number_of_nodes(self):
        # Returns the number of nodes in the graph.
        return len(self.graph.vertices)

    def lcc_size(self):
        # Returns the number of nodes in the largest connected component.
        return len(self.lcc)

    def max_degree(self):
        # Returns the maximum degree of any node in the largest connected component.
        return max(len(self.graph.vertices[node]) for node in self.lcc)

    def average_degree(self):
        # Returns the average degree of nodes in the largest connected component.
        return sum(len(self.graph.vertices[node]) for node in self.lcc) / len(self.lcc)

    def lsp_length(self):
        # Returns the length of the longest simple path found in the LCC.
        return len(self.lsp) - 1

    def print_all_metrics(self, metrics_name):
        # Calculate and return all metrics as a dictionary.
        metrics = {
            f'{metrics_name}':'',
            'n': self.number_of_nodes(),
            '|VLCC|': self.lcc_size(),
            '∆(LCC)': self.max_degree(),
            'k(LCC)': self.average_degree(),
            'Lmax': self.lsp_length(),
        }

        for metric, value in metrics.items():
            print(f"{metric}: {value}")
