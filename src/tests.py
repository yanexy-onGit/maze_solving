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
    def test_maze_reset_visited(self):
        seeds = [-1, 0, 1, 2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 32]
        cell_coords = [
            (0, 0),
            (1, 0),
            (0, 1),
            (6, 11),
            (7, 11),
            (17, 19),
            (0, 19),
            (19, 0)
        ]
        for seed in seeds:
            m = Maze(0, 0, 20, 20, 5, 5, seed=seed)
            m.reset()
            for coords in cell_coords:
                self.assertFalse(m.maze[coords[0]][coords[1]].visited)
            for coords in cell_coords:
                m.maze[coords[0]][coords[1]].visited = True
            for coords in cell_coords:
                self.assertTrue(m.maze[coords[0]][coords[1]].visited)
            m.reset()
            for coords in cell_coords:
                self.assertFalse(m.maze[coords[0]][coords[1]].visited)
            

if __name__ == "__main__":
    unittest.main()