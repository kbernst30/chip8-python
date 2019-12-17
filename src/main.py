from chip8 import Chip8


def load_rom(rom):
    with open("rom/%s" % rom, "rb") as f:
        data = []
        for byte in iter(lambda: f.read(1), b''):
            data.append(byte)

        return [int.from_bytes(d, "big") for d in data]


if __name__ == '__main__':
    chip8 = Chip8(load_rom("TEST"))
    chip8.run()
