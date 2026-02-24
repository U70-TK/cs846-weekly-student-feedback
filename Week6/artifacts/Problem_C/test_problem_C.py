"""
Unit tests for Problem C: Maze Solver
Run with: python3 -m unittest tests.test_problem_C
"""

import unittest
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from problem_C import MazeSolver


# ---------------------------------------------------------------------------
# C_1 — validate() — 5 tests
# ---------------------------------------------------------------------------
class TestValidate(unittest.TestCase):

    def test_valid_simple_maze(self):
        grid = [
            ["S", ".", "#"],
            ["#", ".", "."],
            ["#", "#", "E"],
        ]
        self.assertTrue(MazeSolver(grid).validate())

    def test_invalid_no_start(self):
        grid = [
            [".", ".", "#"],
            ["#", ".", "E"],
        ]
        self.assertFalse(MazeSolver(grid).validate())

    def test_invalid_no_end(self):
        grid = [["S", "."], [".", "."]]
        self.assertFalse(MazeSolver(grid).validate())

    def test_invalid_bad_character(self):
        grid = [["S", "X"], [".", "E"]]
        self.assertFalse(MazeSolver(grid).validate())

    def test_invalid_empty_grid(self):
        self.assertFalse(MazeSolver([]).validate())


# ---------------------------------------------------------------------------
# C_2 — has_path() — 5 tests
# ---------------------------------------------------------------------------
class TestHasPath(unittest.TestCase):

    def test_direct_path(self):
        grid = [
            ["S", ".", "E"],
        ]
        self.assertTrue(MazeSolver(grid).has_path())

    def test_winding_path(self):
        grid = [
            ["S", "#", "E"],
            [".", "#", "."],
            [".", ".", "."],
        ]
        # Path: S→down→down→right→right→up→up = valid
        self.assertTrue(MazeSolver(grid).has_path())

    def test_no_path_blocked(self):
        grid = [
            ["S", "#"],
            ["#", "E"],
        ]
        self.assertFalse(MazeSolver(grid).has_path())

    def test_invalid_maze_returns_false(self):
        grid = [[".", "."]]  # no S or E
        self.assertFalse(MazeSolver(grid).has_path())

    def test_single_step_path(self):
        grid = [["S", "E"]]
        self.assertTrue(MazeSolver(grid).has_path())


# ---------------------------------------------------------------------------
# C_3 — shortest_path_length() — 5 tests
# ---------------------------------------------------------------------------
class TestShortestPath(unittest.TestCase):

    def test_one_step(self):
        grid = [["S", "E"]]
        self.assertEqual(MazeSolver(grid).shortest_path_length(), 1)

    def test_shortest_over_longer_route(self):
        # Two possible paths; shortest is 2 steps (right, right)
        grid = [
            ["S", ".", "E"],
            [".", ".", "."],
        ]
        self.assertEqual(MazeSolver(grid).shortest_path_length(), 2)

    def test_no_path_returns_minus_one(self):
        grid = [
            ["S", "#"],
            ["#", "E"],
        ]
        self.assertEqual(MazeSolver(grid).shortest_path_length(), -1)

    def test_longer_maze(self):
        grid = [
            ["S", ".", ".", "."],
            ["#", "#", "#", "."],
            ["E", ".", ".", "."],
        ]
        # Shortest: S→right×3→down×2→left×3 = 8 steps
        self.assertEqual(MazeSolver(grid).shortest_path_length(), 8)

    def test_invalid_maze_returns_minus_one(self):
        self.assertEqual(MazeSolver([]).shortest_path_length(), -1)


if __name__ == "__main__":
    unittest.main()
