import unittest
from DijkstraMax import DijkstraMax
from Graph import Graph

class TestDijkstraMax(unittest.TestCase):
    def setUp(self):
        # Initialize the graph
        self.graph = Graph()

        edges = [(2, 3), (3, 4), (4, 5), (3, 6), (1, 7), (7, 8),
                 (8, 9), (9, 10), (10, 11), (11, 12)]

        # Add vertices
        for i in range(1, 13):
            self.graph.add_vertex(i)

        for u, v in edges:
            self.graph.add_edge(u, v)

        # Initialize the DijkstraMax algorithm
        self.dijkstra = DijkstraMax(self.graph)

    def test_initialize_single_source_max(self):
        self.dijkstra.initialize_single_source_max(1)
        self.assertEqual(self.dijkstra.distances[1], 0)
        self.assertEqual(self.dijkstra.distances[2], float('-inf'))
        self.assertEqual(self.dijkstra.distances[3], float('-inf'))

    def test_relax_max(self):
        self.dijkstra.initialize_single_source_max(1)
        self.dijkstra.relax_max(1, 2)
        self.assertEqual(self.dijkstra.distances[2], 1)
        self.assertEqual(self.dijkstra.predecessors[2], 1)

    def test_get_longest_path(self):
        # Test finding the longest path in the graph
        longest_path_length, longest_path = self.dijkstra.get_longest_path()
        # Check if the longest path and its length are as expected
        expected_path_length = 6  # This is the number of edges in the longest path [1, 7, 8, 9, 10, 11, 12]
        expected_path = [1, 7, 8, 9, 10, 11, 12]  # One possible longest path

        self.assertEqual(longest_path_length, expected_path_length,
                         "The length of the path did not match the expected value.")
        self.assertEqual(longest_path, expected_path, "The path did not match the expected path.")


if __name__ == '__main__':
    unittest.main()
