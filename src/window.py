from tkinter import Tk, BOTH, Canvas
from time import sleep

class Window:
    def __init__(self, width, height):
        self.__root = Tk()
        self.__root.title("maze solver")
        self.__canvas = Canvas(self.__root, width=width, height=height)
        self.__canvas.pack(fill=BOTH, expand=1)
        self.__running = False
        self.__root.protocol("WM_DELETE_WINDOW", self.close)

    def redraw(self):
        self.__root.update_idletasks()
        self.__root.update()
    
    def wait_for_close(self):
        self.__running = True
        # self.redraw()
        # sleep(1.5)
        # self.close()
        while self.__running:
            self.redraw()
        print("window closed ...")
        
    def close(self):
        self.__running = False

    def draw_line(self, line, fill_clr="black"):
        line.draw(self.__canvas, fill_clr)