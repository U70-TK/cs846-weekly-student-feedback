"""
Problem C: Maze Solver
======================
A maze is a 2D grid of characters:
  '.' - open path
  '#' - wall
  'S' - start (exactly one)
  'E' - end   (exactly one)

Implement the three methods below inside MazeSolver.
Do NOT modify the method signatures.
"""

from collections import deque
from typing import List, Optional


class MazeSolver:
    def __init__(self, grid: List[List[str]]):
        """
        :param grid: 2D list of single characters representing the maze.
        """
        self.grid = grid

    # ------------------------------------------------------------------
    # Problem C_1 — Validate the Maze
    # ------------------------------------------------------------------
    def validate(self) -> bool:
        """
        Return True if the maze is valid, False otherwise.

        A valid maze:
          - Is a non-empty rectangular 2D list
          - Contains exactly one 'S' and exactly one 'E'
          - Contains only '.', '#', 'S', 'E'
        """
        # TODO: Implement this method
        raise NotImplementedError("validate() is not implemented yet.")

    # ------------------------------------------------------------------
    # Problem C_2 — Check if a Path Exists
    # ------------------------------------------------------------------
    def has_path(self) -> bool:
        """
        Return True if any path exists from 'S' to 'E' moving
        up/down/left/right through open cells ('.', 'S', 'E').
        Return False if no path exists or the maze is invalid.

        Hint: BFS or DFS both work here.
        """
        # TODO: Implement this method
        raise NotImplementedError("has_path() is not implemented yet.")

    # ------------------------------------------------------------------
    # Problem C_3 — Shortest Path Length
    # ------------------------------------------------------------------
    def shortest_path_length(self) -> int:
        """
        Return the number of steps in the shortest path from 'S' to 'E'.
        Return -1 if no path exists or the maze is invalid.

        A 'step' is one move to an adjacent cell (up/down/left/right).
        """
        # TODO: Implement this method
        raise NotImplementedError("shortest_path_length() is not implemented yet.")

    # ------------------------------------------------------------------
    # Helper — add any private helpers you need below
    # ------------------------------------------------------------------
    def _find_cell(self, char: str) -> Optional[tuple]:
        """Return (row, col) of the first occurrence of char, or None."""
        for r, row in enumerate(self.grid):
            for c, cell in enumerate(row):
                if cell == char:
                    return (r, c)
        return None
