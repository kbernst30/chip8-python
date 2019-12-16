import random

from util import int_to_hex


class Cpu:

    def __init__(self, mmu, display):
        self.mmu = mmu
        self.display = display

        self.pc = 0
        self.stack = []

        self.primary_op_handlers = {
            0x0: lambda op:  self.zero_prefix_op_handlers[op & 0xFFF](op),
            0x1: self.handle_jump_op,
            0x2: self.handle_call_op,
            0x3: self.handle_truthy_value_condition_op,
            0x4: self.handle_falsey_value_condition_op,
            0x5: self.handle_truthy_register_condition_op,
            0x6: self.handle_set_register_to_value_op,
            0x7: self.handle_add_value_to_register_op,
            0x8: lambda op: self.eight_prefix_op_handlers[op & 0xF](op),
            0x9: self.handle_falsey_register_condition_op,
            0xA: self.handle_address_register_to_value_op,
            0xB: self.handle_jump_with_offset_op,
            0xC: self.handle_set_register_to_random_bitwise_value_op,
            0xD: None,
            0xE: None,
            0xF: None,
        }

        # Ops that start with prefix 0 (i.e. 0x00EE) should lookup here by
        # their last three digits in the hex op
        self.zero_prefix_op_handlers = {
            0x0E0: self.handle_clear_screen_op,
            0x0EE: self.handle_return_op
        }

        # Ops that start with prefix 8 (i.e. 0x8XY0) should lookup here by
        # their last digit in the hex op
        self.eight_prefix_op_handlers = {
            0x0: self.handle_assign_register_to_register_op,
            0x1: self.handle_register_or_register_op,
            0x2: self.handle_register_and_register_op,
            0x3: self.handle_register_xor_register_op,
            0x4: self.handle_add_register_to_register_op,
            0x5: self.handle_subtract_register_y_from_register_x_op,
            0x6: self.handle_bit_shift_right_op,
            0x7: self.handle_subtract_register_x_from_register_y_op,
            0xE: self.handle_bit_shift_left_op,
        }

    def execute(self):
        # All opcodes are big endian
        opcode = self._get_op()

        # Get the prefix and execute corresponding instruction
        prefix = (opcode & 0xF000) >> 12
        self.primary_op_handlers[prefix](opcode)

    def handle_clear_screen_op(self, op):
        '''
        Instruction 0x00E0 - Clears the screen
        '''

        self.display.clear_screen()

    def handle_return_op(self, op):
        '''
        Instruction 0x00EE - Returns from a subroutine
        '''

        address = self.stack.pop()
        self.pc = address

    def handle_jump_op(self, op):
        '''
        Instruction 0x1NNN - Jump to NNN
        '''

        address = op & 0xFFF  # Gets the NNN part of op
        self.pc = address

    def handle_call_op(self, op):
        '''
        Instruction 0x2NNN - Call subroutine at NNN
        '''

        self.stack.append(self.pc)
        self.handle_jump_op(op)

    def handle_truthy_value_condition_op(self, op):
        '''
        Instruction 0x3XNN - Skip next instruction if VX equals NN
        '''

        if self._register_x_equals_nn(op):
            self.pc += 1

    def handle_falsey_value_condition_op(self, op):
        '''
        Instruction 0x3XNN - Skip next instruction if VX doesn't equal NN
        '''

        if not self._register_x_equals_nn(op):
            self.pc += 1

    def handle_truthy_register_condition_op(self, op):
        '''
        Instruction 0x5XY0 - Skip next instruction if VX equals VY
        '''

        if self._register_x_equals_register_y(op):
            self.pc += 1

    def handle_set_register_to_value_op(self, op):
        '''
        Instruction 0x6XNN - Sets VX to NN
        '''

        register = int_to_hex((op & 0xF00) >> 8)
        value = op & 0xFF
        self.mmu.write_register(register, value)

    def handle_add_value_to_register_op(self, op):
        '''
        Instruction - 0x7XNN - Adds NN to VX (Do not set carry flag)
        '''

        register = int_to_hex((op & 0xF00) >> 8)
        value = op & 0xFF
        self.mmu.write_register(
            register,
            self._do_add(
                self.mmu.read_register(register),
                value,
                set_carry=False
            )
        )

    def handle_assign_register_to_register_op(self, op):
        '''
        Instruction - 0x8XY0 - Set VX to value at VY
        '''

        register_x = int_to_hex((op & 0xF00) >> 8)
        register_y = int_to_hex((op & 0xF0) >> 4)
        self.mmu.write_register(
            register_x,
            self.mmu.read_register(register_y)
        )

    def handle_register_or_register_op(self, op):
        '''
        Instruction - 0x8XY1 - Set VX to value of VX OR VY
        '''

        register_x = int_to_hex((op & 0xF00) >> 8)
        register_y = int_to_hex((op & 0xF0) >> 4)
        value = self.mmu.read_register(register_x) | \
            self.mmu.read_register(register_y)

        self.mmu.write_register(register_x, value)

    def handle_register_and_register_op(self, op):
        '''
        Instruction - 0x8XY2 - Set VX to value of VX AND VY
        '''

        register_x = int_to_hex((op & 0xF00) >> 8)
        register_y = int_to_hex((op & 0xF0) >> 4)
        value = self.mmu.read_register(register_x) & \
            self.mmu.read_register(register_y)

        self.mmu.write_register(register_x, value)

    def handle_register_xor_register_op(self, op):
        '''
        Instruction - 0x8XY3 - Set VX to value of VX XOR VY
        '''

        register_x = int_to_hex((op & 0xF00) >> 8)
        register_y = int_to_hex((op & 0xF0) >> 4)
        value = self.mmu.read_register(register_x) ^ \
            self.mmu.read_register(register_y)

        self.mmu.write_register(register_x, value)

    def handle_add_register_to_register_op(self, op):
        '''
        Instruction - 0x8XY4 - Adds VY to VX and stores it in VX
        Stores carry flag as needed
        '''

        register_x = int_to_hex((op & 0xF00) >> 8)
        register_y = int_to_hex((op & 0xF0) >> 4)
        self.mmu.write_register(
            register_x,
            self._do_add(
                self.mmu.read_register(register_x),
                self.mmu.read_register(register_y),
            )
        )

    def handle_subtract_register_y_from_register_x_op(self, op):
        '''
        Instruction - 0x8XY5 - Subtracts VY from VX and stores in VX
        Stores carry flag as needed (borrow)
        '''

        register_x = int_to_hex((op & 0xF00) >> 8)
        register_y = int_to_hex((op & 0xF0) >> 4)
        self.mmu.write_register(
            register_x,
            self._do_subtract(
                self.mmu.read_register(register_x),
                self.mmu.read_register(register_y),
            )
        )

    def handle_bit_shift_right_op(self, op):
        '''
        Instruction - 0x8XY6 - Stores least significant bit of VX in VF
        and shifts VX right by 1
        '''

        register_x = int_to_hex((op & 0xF00) >> 8)
        bit = self.mmu.read_register(register_x) & 0x1
        self.mmu.write_register('F', bit)
        self.mmu.write_register(
            register_x,
            self.mmu.read_register(register_x) >> 1
        )

    def handle_subtract_register_x_from_register_y_op(self, op):
        '''
        Instruction - 0x8XY7 - Subtracts VX from VY and stores in VX
        Stores carry flag as needed (borrow)
        '''

        register_x = int_to_hex((op & 0xF00) >> 8)
        register_y = int_to_hex((op & 0xF0) >> 4)
        self.mmu.write_register(
            register_x,
            self._do_subtract(
                self.mmu.read_register(register_y),
                self.mmu.read_register(register_x),
            )
        )

    def handle_bit_shift_left_op(self, op):
        '''
        Instruction - 0x8XYE - Stores least significant bit of VX in VF
        and shifts VX left by 1
        '''

        register_x = int_to_hex((op & 0xF00) >> 8)
        bit = self.mmu.read_register(register_x) & 0x1
        self.mmu.write_register('F', bit)
        self.mmu.write_register(
            register_x,
            self.mmu.read_register(register_x) << 1
        )

    def handle_falsey_register_condition_op(self, op):
        '''
        Instruction 0x9XY0 - Skip next instruction if VX deosn't equal VY
        '''

        if not self._register_x_equals_register_y(op):
            self.pc += 1

    def handle_address_register_to_value_op(self, op):
        '''
        Instruction 0xANNN - Sets I to address NNN
        '''

        address = op & 0xFFF  # Gets the NNN part of op
        self.mmu.write_address_register(address)

    def handle_jump_with_offset_op(self, op):
        '''
        Instruction - 0xBNNN - Jump to address NNN plus value at V0
        '''

        value = self.mmu.read_register('0')
        address = (op & 0xFFF) + value
        self.pc = address

    def handle_set_register_to_random_bitwise_value_op(self, op):
        '''
        Instruction - 0xCXNN - Set VX to result of bitwise AND of NN and
        random number from 0-255
        '''

        register = int_to_hex((op & 0xF00) >> 8)
        value = op & 0xFF
        rand = random.randint(0, 255)
        self.mmu.write_register(register, value & rand)

    def _get_op(self):
        first = self.mmu.read(self.pc)
        self.pc += 1
        second = self.mmu.read(self.pc)
        self.pc += 1

        return (first << 8) | second

    def _register_x_equals_nn(self, op):
        '''
        Returns true if value at register X equals NN
        OP is in form: 0xZXNN
        '''

        register = int_to_hex((op & 0xF00) >> 8)
        value = op & 0xFF
        return self.mmu.read_register(register) == value

    def _register_x_equals_register_y(self, op):
        '''
        Returns true if value at register X equals value at register Y
        OP is in form: 0xZXY0
        '''

        register_x = int_to_hex((op & 0xF00) >> 8)
        register_y = int_to_hex((op & 0xF0) >> 4)
        return self.mmu.read_register(register_x) == \
            self.mmu.read_register(register_y)

    def _do_add(self, v1, v2, set_carry=True):
        val = v1 + v2

        # Deal with overflow - Adding two 8 bit numbers so if we exceed
        # the max capacity for 1 byte (i.e. 255) we need to deal with the
        # excess and set carry flag if needed
        if val > 0xFF:
            val -= 0xFF - 1  # Overflows back around
            if set_carry:
                self.mmu.write_register('F', 1)

        elif set_carry:
            self.mmu.write_register('F', 0)

        return val

    def _do_subtract(self, v1, v2, set_borrow=True):
        val = v1 - v2

        # Deal with the underflow - Substracting one 8 bit number from another
        # can result in a value under 0, which would mean we would need to
        # "borrow". We need to deal with the underflow and set carry flag
        # if needed (if we borrowed)

        if val < 0:
            val += 0xFF + 1
            if set_borrow:
                self.mmu.write_register('F', 1)

        elif set_borrow:
            self.mmu.write_register('F', 0)

    def test(self):
        self.primary_op_handlers[0x1](0x1DDD)
