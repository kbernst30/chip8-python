class Mmu:

    def __init__(self):
        # Chip 8 has 0x1000 (4096) memory locations
        # Each memory location is 8-bits (one byte)
        # The uppermost 256 bytes (0xF00-0xFFF) are for display refresh,
        # 96 bytes below that (0xEA0-0xEFF) were for the call stack,
        # internal use, and other variables.
        self.memory = [0 for i in range(0x1000)]

        # 16 8-bit registers - V0 - VF
        self.registers = {
            'V0': 0,
            'V1': 0,
            'V2': 0,
            'V3': 0,
            'V4': 0,
            'V5': 0,
            'V6': 0,
            'V7': 0,
            'V8': 0,
            'V9': 0,
            'VA': 0,
            'VB': 0,
            'VC': 0,
            'VD': 0,
            'VE': 0,
            'VF': 0
        }

        # Address register I is 16 bits
        self.address_register = 0

    def read_register(self, reg):
        pass

    def write_register(self, reg, value):
        pass

    def read_address_register(self):
        pass

    def write_address_register(self, value):
        pass

    def read(self, address):
        pass

    def write(self, address, value):
        pass
