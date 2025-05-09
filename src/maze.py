from strokes import Point, Line
from time import sleep

class Maze:
    def __init__(self, x, y, rows_count, cols_count, cell_size_x, cell_size_y, window=None):
        self.x = x
        self.y = y
        self.rows_count = int(rows_count)
        self.cols_count = int(cols_count)
        self.cell_size_x = cell_size_x
        self.cell_size_y = cell_size_y
        self.window = window
        self.maze = [[None]*self.cols_count for _ in range(self.rows_count)]
        self.__create_cells()

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
        for i in range(4):
            if self.has_wall_left_clockwise[i]:
                self.__window.draw_line(self.__wall_lines[i])
    
    def toggle_wall(self, *keys):
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

    def __get_centre_p(self):
        return Point(self.__x+.5*self.size, self.__y+.5*self.size)
    
    def draw_move(self, to_cell, undo=False):
        clr = (undo and "red") or "gray"
        self.__window.draw_line(Line(self.__get_centre_p(), to_cell.__get_centre_p()), clr)