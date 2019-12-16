import tkinter
import time

from cpu import Cpu
from display import Display
from keyboard import Keyboard
from mmu import Mmu


class Chip8:

    DISPLAY_SCALE = 10

    def __init__(self, rom):
        self.display = Display()
        self.keyboard = Keyboard()
        self.mmu = Mmu()

        self.mmu.load_rom(rom)
        self.cpu = Cpu(self.mmu, self.display, self.keyboard)

        self.window = self._init_canvas()

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

        # Main emu loop
        while True:
            if not self.cpu.halted:
                debug = self.cpu.execute()
                # print(debug)

                # Update screen
                self._update_canvas()
                self.window.update()

                # Update timers
                self.mmu.update_delay_timer()
                self.mmu.update_sound_timer()
            else:
                print("HALTED")

            time.sleep(1 / 60)  # 60 fps
            # time.sleep(0.1)

    def _init_canvas(self):
        window = tkinter.Tk()

        canvas_width = self.display.width * self.DISPLAY_SCALE
        canvas_height = self.display.height * self.DISPLAY_SCALE

        def on_key_down(e):
            print("DEBUG")
            self.keyboard.press(e.char, self.cpu.on_unhalt)
            self.cpu.halted = False

        def on_key_up(e):
            self.keyboard.unpress(e.char)

        window.bind('<KeyPress>', on_key_down)
        window.bind('<KeyRelease>', on_key_up)

        self.canvas = tkinter.Canvas(
            window,
            width=canvas_width,
            height=canvas_height
        )

        self.canvas.pack()

        return window

    def _update_canvas(self):
        for x in range(self.display.width):
            for y in range(self.display.height):
                self.canvas.create_rectangle(
                    x * self.DISPLAY_SCALE,
                    y * self.DISPLAY_SCALE,
                    (x * self.DISPLAY_SCALE) + self.DISPLAY_SCALE,
                    (y * self.DISPLAY_SCALE) + self.DISPLAY_SCALE,
                    fill="#000000" if self.display.get_pixel(x, y) == 0 else '#FFFFFF'
                )
