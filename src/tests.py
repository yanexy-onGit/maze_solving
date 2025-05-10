import unittest
from maze import Maze

class Tests(unittest.TestCase):
    def test_maze_create_cells(self):
        test_sizes = [
            [12, 10],
            [1, 8],
            [16, 16]
        ]
        for case_size in test_sizes:
            m = Maze(0, 0, case_size[0], case_size[1], 10, 10)
            self.assertEqual(
                len(m.maze),
                case_size[0],
            )
            self.assertEqual(
                len(m.maze[0]),
                case_size[1],
            )

if __name__ == "__main__":
    unittest.main()