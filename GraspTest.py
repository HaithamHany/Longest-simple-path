import unittest
from Grasp import Grasp
from Graph import Graph  # Assuming Graph is a class you have already implemented


class TestGRASP(unittest.TestCase):
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

        # Initialize the GRASP algorithm with the graph and LCC
        self.grasp = Grasp(self.graph, lcc)

    def test_get_candidates(self):
        # Test the get_candidates method to verify it returns the correct candidates
        current_node = 1
        path = [1]
        candidates = self.grasp.get_candidates(current_node, path)

        # Expected candidates from node 1 in the example graph: [7]
        expected_candidates = [7]

        self.assertEqual(candidates, expected_candidates,
                         f"Candidates from {current_node} did not match expected candidates")

    def test_greedy_randomized_construction(self):
        # Test the greedy_randomized_construction method
        path = self.grasp.greedy_randomized_construction()

        # Check the path returned is not empty
        self.assertTrue(len(path) > 0, "Path should not be empty")

        # Check that the path contains unique nodes and starts with a node from the graph
        start_node = path[0]
        self.assertIn(start_node, self.graph.vertices, "Start node should be a vertex in the graph")
        self.assertEqual(len(path), len(set(path)), "Path should not contain duplicate nodes")

    def test_local_search(self):
        # Test the local_search method with a predefined path
        path = [1, 7, 8, 9, 10, 11, 12]  # Example path from 1 to 12
        improved_path = self.grasp.local_search(path)

        # Verify the improved path length is at least the same as the original path
        self.assertTrue(len(improved_path) >= len(path), "Local search should not shorten the path")

    def test_grasp_longest_path(self):
        # Test the grasp_longest_path method
        longest_path = self.grasp.grasp_longest_path()

        # Verify the path is not empty
        self.assertTrue(len(longest_path) > 0, "Longest path should not be empty")

        # Verify that the path contains unique nodes
        self.assertEqual(len(longest_path), len(set(longest_path)), "Longest path should not contain duplicate nodes")


if __name__ == '__main__':
    unittest.main()
