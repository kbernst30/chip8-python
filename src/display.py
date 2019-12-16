class Display:

    def __init__(self):
        self.width = 64
        self.height = 32

        self.clear_screen()

    def clear_screen(self):
        self.screen = [
            [0 for y in range(self.height)] for x in range(self.width)
        ]
