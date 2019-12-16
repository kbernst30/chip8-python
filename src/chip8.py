import tkinter

from display import Display
from mmu import Mmu


class Chip8:

    DISPLAY_SCALE = 10

    def __init__(self):
        self.display = Display()
        self.mmu = Mmu()

        self._init_canvas()

    def run(self):
        y = 20
        for x in range(self.display.width):
            for y in range(self.display.height):
                self.canvas.create_rectangle(
                    x * self.DISPLAY_SCALE,
                    y * self.DISPLAY_SCALE,
                    (x * self.DISPLAY_SCALE) + self.DISPLAY_SCALE,
                    (y * self.DISPLAY_SCALE) + self.DISPLAY_SCALE,
                    fill="#000000"
                )

        tkinter.mainloop()

    def _init_canvas(self):
        window = tkinter.Tk()

        canvas_width = self.display.width * self.DISPLAY_SCALE
        canvas_height = self.display.height * self.DISPLAY_SCALE

        self.canvas = tkinter.Canvas(
            window,
            width=canvas_width,
            height=canvas_height
        )

        self.canvas.pack()
