class Keyboard:
    '''
    Represents a Hex Keyboard for the Chip-8 inpupt
    There are 16 keys, 0-F

    Key Mapping is as follows to QWERTY

    1=1 2=2 3=3 4=C
    q=4 w=5 e=6 r=D
    a=7 s=8 d=9 f=E
    z=A x=0 c=B v=F
    '''

    def __init__(self):
        self.input = [0 for i in range(0xF)]

        self.key_mappings = {
            '1': 0x1,
            '2': 0x2,
            '3': 0x3,
            '4': 0xC,
            'q': 0x4,
            'w': 0x5,
            'e': 0x6,
            'r': 0xD,
            'a': 0x7,
            's': 0x8,
            'd': 0x9,
            'f': 0xE,
            'z': 0xA,
            'x': 0x0,
            'c': 0xB,
            'v': 0xF
        }

    def press(self, key, callback=None):
        if key in self.key_mappings:
            if self.input[self.key_mappings[key]] == 0:
                self.input[self.key_mappings[key]] = 1

            if callback is not None:
                callback(self.key_mappings[key])

    def unpress(self, key):
        if key in self.key_mappings:
            if self.input[self.key_mappings[key]] == 1:
                self.input[self.key_mappings[key]] = 0

    def is_pressed(self, key):
        return self.input[key] == 1
