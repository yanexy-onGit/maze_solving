from strokes import Point, Line
from time import sleep
from random import seed, randint, shuffle

class Maze:
    def __init__(self, x, y, rows_count, cols_count, cell_size_x, cell_size_y, window=None, seed=None):
        self.__testing_fcall_count = 0
        self.x = x
        self.y = y
        self.rows_count = int(rows_count)
        self.cols_count = int(cols_count)
        self.cell_size_x = cell_size_x
        self.cell_size_y = cell_size_y
        self.window = window
        self.__seed = seed
        self.maze = [[None]*self.cols_count for _ in range(self.rows_count)]
        self.__create_cells()
        self.__break_entrance_and_exit()
        self.__mazefy()

    # ? discard
    def reset(self):
        self.maze = [[None]*self.cols_count for _ in range(self.rows_count)]
        self.__create_cells()

    def cell_at(self, coordinates):
        if not self.__coordinates_valid(*coordinates):
            return None
        return self.maze[coordinates[0]][coordinates[-1]]
        
    # tested!
    def __break_entrance_and_exit(self):
        first_cell, last_cell = [self.maze[0][0], self.maze[-1][-1]]
        first_cell.toggle_wall(randint(0, 1))
        last_cell.toggle_wall(randint(2, 3), visit=False)
    
    # tested!
    def __coordinates_valid(self, row_idx, col_idx):
        if row_idx in range(self.rows_count) and col_idx in range(self.cols_count):
            return True
        return False

    # tested!
    def __cross_by_direction(self, coordinates, direction):
        if type(direction) == str:
            idx_dict = { "l": 0, "u": 1, "r": 2, "d": 3 }
            break_at_idx= idx_dict.get(direction[0], None)
        elif type(direction) == int:
            break_at_idx= direction 
        if break_at_idx == None:
            raise ValueError("invalid direction")
        if self.__coordinates_valid(*coordinates):
            row_idx, col_idx = coordinates
            new_coordinates = [(row_idx, col_idx-1), (row_idx-1, col_idx), (row_idx, col_idx+1), (row_idx+1, col_idx)][break_at_idx]
        if self.__coordinates_valid(*new_coordinates):
            self.cell_at(coordinates).toggle_wall(break_at_idx)
            self.cell_at(new_coordinates).toggle_wall((break_at_idx+2)%4)
            return new_coordinates
        return None
    
    # ? test
    def __cross(self, coords_from, coords_to):
        row_idx, col_idx = coords_from
        direction = [(row_idx, col_idx-1), (row_idx-1, col_idx), (row_idx, col_idx+1), (row_idx+1, col_idx), coords_to].index(coords_to)
        # testing_dict = ["left", "up", "right", "down"]
        # print(f"__cross-ing from {coords_from} in direction {testing_dict[direction]}")
        if direction > 3:
            raise Exception("cells to be crossed between must be adjacent")
        return self.__cross_by_direction(coords_from, direction=direction)

    def __undo_cross(self, coords_from, coords_to):
        pass

    # ? test
    def cell_adjacents(self, coordinates, ignore_visited=False):
        row_idx, col_idx = coordinates
        adjacents = [coords for coords in [(row_idx, col_idx-1), (row_idx-1, col_idx), (row_idx, col_idx+1), (row_idx+1, col_idx)] if self.__coordinates_valid(*coords)]
        if ignore_visited:
            adjacents = [coords for coords in adjacents if not self.cell_at(coords).visited]
        return adjacents

    # ? test
    def create_solution_from(self, coordinates=(0, 0)):
        if coordinates == (self.rows_count-1, self.cols_count-1):
            return 0
        adjacents = self.cell_adjacents(coordinates, ignore_visited=True)
        print(f"{coordinates} adjacents are: {adjacents}")
        if not adjacents:
            return -1
        shuffle(adjacents)
        for adjace_coords in adjacents:
            self.__cross(coordinates, adjace_coords)
            res = self.create_solution_from(adjace_coords)
            if res == 0:
                return 0
            # self.cell_at(adjace_coords).reset_walls()
            # self.cell_at(adjace_coords).set_unvisited()
            # self.cell_at(coordinates).reset_walls()
        return -2
    
    # ? test
    def scramble(self):
        unvisited = []
        for row_idx in range(self.rows_count):
            for col_idx in range(self.cols_count):
                coords = (row_idx, col_idx)
                self.cell_at(coords).visited or unvisited.append(coords)
        while len(unvisited) > 1:
            coords = unvisited.pop()
            adjacents = self.cell_adjacents(coords)
            shuffle(adjacents)
            adjacents = adjacents[:2]
            unvisited = [unvis_coords for unvis_coords in unvisited if not unvis_coords in adjacents]
            for adjace_coords in adjacents:
                self.__cross(coords, adjace_coords)
        if unvisited:
            adjacents = self.cell_adjacents(unvisited[0])
            shuffle(adjacents)
            self.__cross(unvisited[0], adjacents[0])



    # ? test
    def __mazefy(self):
        if self.__seed != None:
            seed(self.__seed)
        res = self.create_solution_from((0, 0))
        print(res)
        self.scramble()
        

    def __create_cells(self):
        # populating
        y = self.y
        for row in self.maze:
            x = self.x
            for i in range(self.cols_count):
                row[i] = Cell(x, y, self.window, self.cell_size_x)
                x += self.cell_size_x
            y += self.cell_size_y

        # drawing
        if self.window == None:
            print("skip drawing of maze: no window object provided")
            return
        
        for i in range(self.rows_count):
            for j in range(self.cols_count):
                self.maze[i][j].draw()
                
        self.__animate()
    

    def __animate(self):
        self.window.redraw()
        sleep(.05)



class Cell:
    __size = 10
    def __init__(self, x, y, window=None, size=0):
        self.size = size or Cell.__size
        self.has_wall_left_clockwise = [True] * 4
        self.visited = False
        corners = [
            Point(x, y),
            Point(x+self.size, y),
            Point(x+self.size, y+self.size),
            Point(x, y+self.size)
        ]
        self.__wall_lines = [Line(corners[i-1], corners[(i)%4]) for i in range(4)]
        self.__window = window
        self.__x = x
        self.__y = y

    def draw(self):
        if self.__window == None:
            return
        for i in range(4):
            clr = self.has_wall_left_clockwise[i] and "black" or "#d9d9d9"
            self.__window.draw_line(self.__wall_lines[i], clr)            
    
    def toggle_wall(self, *keys, visit=True):
        keys = set(keys)
        for key in keys:
            idx = None
            if type(key) == str:
                idx_dict = { "l": 0, "t": 1, "r": 2, "b": 3 }
                idx = idx_dict.get(key[0], None)
            elif type(key) == int:
                idx = key 
            if idx != None:
                self.has_wall_left_clockwise[idx%4] = not self.has_wall_left_clockwise[idx%4]
        if visit:
            self.visited = True
        self.draw()

    def reset_walls(self):
        self.has_wall_left_clockwise = [True] * 4
        self.draw()
    
    def set_unvisited(self):
        self.visited = False

    def __get_centre_p(self):
        return Point(self.__x+.5*self.size, self.__y+.5*self.size)
    
    def draw_move(self, to_cell, undo=False):
        clr = (undo and "red") or "gray"
        self.__window.draw_line(Line(self.__get_centre_p(), to_cell.__get_centre_p()), clr)