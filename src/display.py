class Display:

    def __init__(self):
        self.width = 64
        self.height = 32

        self.clear_screen()

    def clear_screen(self):
        self.screen = [
            [0 for y in range(self.height)] for x in range(self.width)
        ]

    def set_pixel(self, x, y, value):
        original = self.screen[x][y]

        # We flip the color of the screen pixel if sprite
        # pixel is set
        new_val = original ^ value
        self.screen[x][y] = new_val

        # Return if we flipped the screen pixel or not
        return original != new_val

    def get_pixel(self, x, y):
        return self.screen[x][y]

    def get_set_pixels(self):
        pixels = []
        for x in range(self.width):
            for y in range(self.height):
                if self.screen[x][y] == 1:
                    pixels.append((x, y))

        return pixels
