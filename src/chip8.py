import sys
import pygame
import pygame.locals

from cpu import Cpu
from display import Display
from keyboard import Keyboard
from mmu import Mmu


class Chip8:

    DISPLAY_SCALE = 10
    TIMER = pygame.USEREVENT + 1

    def __init__(self, rom):
        self.debug = []
        self.display = Display()
        self.keyboard = Keyboard()
        self.mmu = Mmu()

        self.mmu.load_rom(rom)
        self.cpu = Cpu(self.mmu, self.display, self.keyboard)

        pygame.init()

        self.font = pygame.font.SysFont("monospace", 20)
        self.window = self._init_canvas()

        self.debug = True

    def run(self):
        # Main emu loop
        pygame.time.set_timer(self.TIMER, 17)  # ~60 Hz

        while True:
            self.cpu.execute()

            # Update screen
            self._update_screen()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    sys.exit()
                elif event.type == self.TIMER:
                    self.mmu.update_delay_timer()
                    self.mmu.update_sound_timer()

    def _init_canvas(self):
        width = self.display.width * self.DISPLAY_SCALE
        height = self.display.height * self.DISPLAY_SCALE
        if self.debug:
            height += 500

        size = width, height
        window = pygame.display.set_mode(size, pygame.locals.DOUBLEBUF)
        window.set_alpha(None)
        pygame.display.flip()

        self.canvas = pygame.display.get_surface()
        self.canvas.fill((0, 0, 0))

        return window

    def _update_screen(self):
        self.canvas.fill((0, 0, 0))
        rects = []

        for pixel in self.display.get_set_pixels():
            x = pixel[0]
            y = pixel[1]

            rect = pygame.draw.rect(self.canvas, (255, 255, 255), (
                x * self.DISPLAY_SCALE,
                y * self.DISPLAY_SCALE,
                self.DISPLAY_SCALE,
                self.DISPLAY_SCALE,
            ))

            rects.append(rect)

        if self.debug:
            registers = list(self.mmu.registers.keys())
            lbls = []
            for i in range(len(registers)):
                reg = self.mmu.registers[registers[i]]
                val = (registers[i], "{0:02x}".format(reg))
                lbl = self.font.render("%s - %s" % val, 1, (255, 255, 255))
                x, y = 10, (i * 20) + (self.display.height * self.DISPLAY_SCALE) + 10
                self.canvas.blit(lbl, (x, y))
                lbls.append(lbl)

        pygame.display.flip()
