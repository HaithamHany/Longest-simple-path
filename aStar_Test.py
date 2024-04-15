import unittest
from aStar import aStar
from Graph import Graph  # Assuming Graph is a class you have already implemented


class TestAStar(unittest.TestCase):
    def setUp(self):
        # Initialize the graph
        self.graph = Graph()

        # Define edges to create a specific graph structure
        edges = [(2, 3), (3, 4), (4, 5), (3, 6), (1, 7), (7, 8),
                 (8, 9), (9, 10), (10, 11), (11, 12)]

        # Add vertices
        for i in range(1, 13):
            self.graph.add_vertex(i)

        # Add edges to the graph
        for u, v in edges:
            self.graph.add_edge(u, v)

        # Assume lcc is a list of vertices representing the largest connected component (LCC)
        # In this case, we'll use all the vertices as the LCC for simplicity
        lcc = list(range(1, 13))

        # Initialize the aStar algorithm with the graph and LCC
        self.astar = aStar(self.graph, lcc)

    def test_a_star_longest_path(self):
        # Test the a_star_longest_path method for finding the longest path between two vertices
        start_vertex = 1
        end_vertex = 12
        path = self.astar.a_star_longest_path(start_vertex, end_vertex)

        # Expected path from 1 to 12: 1 -> 7 -> 8 -> 9 -> 10 -> 11 -> 12
        expected_path = [1, 7, 8, 9, 10, 11, 12]

        # Verify the path returned is the expected path
        self.assertEqual(path, expected_path,
                         f"Path from {start_vertex} to {end_vertex} did not match the expected path")

    def test_find_longest_simple_path(self):
        # Test the find_longest_simple_path method for finding the longest simple path in the graph
        longest_path_length, longest_path = self.astar.find_longest_simple_path()

        # Expected longest path length: 6 (from 1 to 12, as per the graph edges defined in setUp)
        expected_path_length = 7
        expected_path = [1, 7, 8, 9, 10, 11, 12]  # Same as the test_a_star_longest_path test

        # Verify the longest path length and path
        self.assertEqual(len(longest_path), expected_path_length, "Longest path length did not match expected length")
        self.assertEqual(longest_path, expected_path, "Longest path did not match expected path")


if __name__ == '__main__':
    unittest.main()