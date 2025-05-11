from window import Window
from strokes import Point, Line
from maze import Maze

def main():
    ONE_SIZE = 1000
    WIN_WIDTH = ONE_SIZE or 450
    WIN_HEIGHT = ONE_SIZE or 450
    CELL_SIZE = 50
    win = Window(WIN_WIDTH, WIN_WIDTH)
    m = Maze(1, 1, WIN_WIDTH/CELL_SIZE, WIN_HEIGHT/CELL_SIZE, CELL_SIZE, CELL_SIZE, win)
    print(m.solve())
    win.wait_for_close()
    

def draw_cross(window, win_width, win_height):
    top_left = Point(0, 0)
    top_right = Point(win_width, 0)
    bottom_right = Point(win_width, win_height)
    bottom_left = Point(0, win_height)
    center = Point(.5*win_width, .5*win_height)
    line_a = Line(top_left, center)
    line_b = Line(top_right, center)
    line_c = Line(bottom_right, center)
    line_d = Line(bottom_left, center)
    window.draw_line(line_a)
    window.draw_line(line_b)
    window.draw_line(line_c)
    window.draw_line(line_d)

if __name__ == "__main__":
    main()

