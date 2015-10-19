from .value import Value


class Instruction(object):
    Input = 0
    Output = 1
    CopyFrom = 2
    CopyTo = 3
    Add = 4
    Sub = 5
    BumpUp = 6
    BumpDown = 7
    Jump = 8
    JumpIfZero = 9
    JumpIfNegative = 10

    def __init__(self, opcode):
        self._opcode = opcode

    @property
    def opcode(self):
        return self._opcode

    def execute(self, machine):
        machine.advance()

    @property
    def opcode_string(self):
        return {
            Instruction.Input: "input",
            Instruction.Output: "output",
            Instruction.CopyFrom: "copy from",
            Instruction.CopyTo: "copy to",
            Instruction.Add: "add",
            Instruction.Sub: "sub",
            Instruction.BumpUp: "bump+",
            Instruction.BumpDown: "bump-",
            Instruction.Jump: "jump",
            Instruction.JumpIfZero: "jumpz",
            Instruction.JumpIfNegative: "jumpn",
        }[self._opcode]


class InstInput(Instruction):
    def __init__(self):
        super().__init__(Instruction.Input)

    def execute(self, machine):
        machine.set_accumulator(machine.read_input())
        machine.advance()


class InstOutput(Instruction):
    def __init__(self):
        super().__init__(Instruction.Output)

    def execute(self, machine):
        machine.write_output(machine.get_accumulator())
        machine.clear_accumulator()
        machine.advance()


class MemoryInstruction(Instruction):
    def __init__(self, opcode, address, indirection):
        super().__init__(opcode)
        self._address = address
        self._indirection = indirection

    @property
    def address(self):
        return self._address

    @property
    def indirection(self):
        return self._indirection

    def execute(self, machine):
        address = self.address
        if self.indirection:
            address = machine.read(address)
        self._mem_execute(machine, address)
        machine.advance()

    def _mem_execute(self, machine, address):
        pass


class InstCopyFrom(MemoryInstruction):
    def __init__(self, address, indirection):
        super().__init__(Instruction.CopyFrom, address, indirection)

    def _mem_execute(self, machine, address):
        machine.set_accumulator(machine.read(address))


class InstCopyTo(MemoryInstruction):
    def __init__(self, address, indirection):
        super().__init__(Instruction.CopyTo, address, indirection)

    def _mem_execute(self, machine, address):
        machine.write(machine.get_accumulator(), address)


class InstAdd(MemoryInstruction):
    def __init__(self, address, indirection):
        super().__init__(Instruction.Add, address, indirection)

    def _mem_execute(self, machine, address):
        machine.set_accumulator(
            machine.get_accumulator() + machine.read(address)
        )


class InstSub(MemoryInstruction):
    def __init__(self, address, indirection):
        super().__init__(Instruction.Sub, address, indirection)

    def _mem_execute(self, machine, address):
        machine.set_accumulator(
            machine.get_accumulator() - machine.read(address)
        )


class InstBumpUp(MemoryInstruction):
    def __init__(self, address, indirection):
        super().__init__(Instruction.BumpUp, address, indirection)

    def _mem_execute(self, machine, address):
        value = machine.read(address) + Value(1)
        machine.write(value, address)
        machine.set_accumulator(value)


class InstBumpDown(MemoryInstruction):
    def __init__(self, address, indirection):
        super().__init__(Instruction.BumpDown, address, indirection)

    def _mem_execute(self, machine, address):
        value = machine.read(address) - Value(1)
        machine.write(value, address)
        machine.set_accumulator(value)


class JumpInstruction(Instruction):
    def __init__(self, opcode, jump_target):
        super().__init__(opcode)
        self._jump_target = jump_target

    @property
    def jump_target(self):
        return self._jump_target

    def execute(self, machine):
        if self._condition(machine):
            machine.jump(self.jump_target)
        else:
            machine.advance()

    def _condition(self, machine):
        return True


class InstJump(JumpInstruction):
    def __init__(self, jump_target):
        super().__init__(Instruction.Jump, jump_target)


class InstJumpIfZero(JumpInstruction):
    def __init__(self, jump_target):
        super().__init__(Instruction.JumpIfZero, jump_target)

    def _condition(self, machine):
        return machine.get_accumulator().value == 0


class InstJumpIfNegative(JumpInstruction):
    def __init__(self, jump_target):
        super().__init__(Instruction.JumpIfNegative, jump_target)

    def _condition(self, machine):
        return machine.get_accumulator().value < 0


