import signal
import sys
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

        self.x = []

    def run(self):
        # Main emu loop

        # DEBUG STUFF FOR TIMING
        def signal_handler(sig, frame):
            print(self.x[0:61])
            sys.exit(0)

        signal.signal(signal.SIGINT, signal_handler)
        millis = int(round(time.time() * 1000))
        self.x.append(0)

        while True:
            if not self.cpu.halted:
                debug = self.cpu.execute()
                print(debug)

                # Update screen
                self._update_canvas()
                self.window.update()

                # Update timers
                self.mmu.update_delay_timer()
                self.mmu.update_sound_timer()
            else:
                print("HALTED")

            time.sleep(1 / 60)  # 60 fps

            # ADD UPDATED TIME TO DEBUG
            self.x.append(int(round(time.time() * 1000)) - millis)

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

        self.canvas.configure(background='black')
        self.canvas.pack()

        return window

    def _update_canvas(self):
        self.canvas.delete("all")
        for pixel in self.display.get_set_pixels():
            x = pixel[0]
            y = pixel[1]
            self.canvas.create_rectangle(
                x * self.DISPLAY_SCALE,
                y * self.DISPLAY_SCALE,
                (x * self.DISPLAY_SCALE) + self.DISPLAY_SCALE,
                (y * self.DISPLAY_SCALE) + self.DISPLAY_SCALE,
                fill='#FFFFFF'
            )
