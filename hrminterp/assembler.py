from . import instructions
from .value import Value


def assemble_bytecode(parsed):
    assembler = Assembler(parsed)
    return assembler.assemble()


class Assembler(object):
    def __init__(self, parsed):
        self._parsed = parsed

    def assemble(self):
        return tuple(map(self.assemble_inst, self._parsed.instructions))

    def assemble_inst(self, instruction):
        opcode = instruction[0].lower()
        assemble_fn, classname = {
            'inbox': (None, instructions.InstInput),
            'outbox': (None, instructions.InstOutput),
            'copyfrom': (self.asm_meminst, instructions.InstCopyFrom),
            'copyto': (self.asm_meminst, instructions.InstCopyTo),
            'add': (self.asm_meminst, instructions.InstAdd),
            'sub': (self.asm_meminst, instructions.InstSub),
            'bumpup': (self.asm_meminst, instructions.InstBumpUp),
            'bumpdn': (self.asm_meminst, instructions.InstBumpDown),
            'jump': (self.asm_jump, instructions.InstJump),
            'jumpz': (self.asm_jump, instructions.InstJumpIfZero),
            'jumpn': (self.asm_jump, instructions.InstJumpIfNegative),
        }[opcode]

        # print("assembling {}: {}".format(opcode, instruction[1:]))

        if assemble_fn is None:
            return classname()
        else:
            return assemble_fn(classname, instruction)

    def asm_meminst(self, classname, instruction):
        if len(instruction) < 2:
            raise Exception("memory instruction without address parameter")
        address_str = instruction[1]
        indirection = False
        if address_str.startswith("[") and address_str.endswith("]"):
            indirection = True
            address_str = address_str[1:-1]
        try:
            address = Value(int(address_str))
        except Exception as ex:
            raise Exception("invalid address param to memory instruction: {}".format(ex))
        return classname(address, indirection)


    def asm_jump(self, classname, instruction):
        if len(instruction) < 2:
            raise Exception("jump instruction without jump target")
        jump_label = instruction[1]
        if jump_label not in self._parsed.labels:
            raise Exception("jump to invalid label: {}".format(jump_label))
        return classname(self._parsed.labels[jump_label])

