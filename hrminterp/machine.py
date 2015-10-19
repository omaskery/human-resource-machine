from . import instructions


class Machine(object):
    def __init__(self, io_in, io_out, memory_size):
        self._in = io_in
        self._out = io_out
        self._memory = [0 for _ in range(memory_size)]
        self._program = [instructions.InstJump(0)]
        self._code_pointer = 0
        self._accumulator = None
        self._cycles = 0

    def run(self, stop_condition=None):
        if stop_condition is None:
            stop_condition = lambda x: False

        try:
            while not stop_condition(self):
                self.step()
        except KeyboardInterrupt:
            pass

    def step(self):
        instruction = self._program[self._code_pointer]
        # print("{} [{}]: {}".format(self._cycles, self._code_pointer, instruction.opcode_string))
        instruction.execute(self)
        self._cycles += 1

    def set_program(self, program):
        self._program = tuple(program)

    def fill_memory(self, image):
        self._memory = list(image[:len(self._memory)])

    def set_accumulator(self, value):
        # print("accumulator is now {}".format(value))
        self._accumulator = value

    def get_accumulator(self):
        if self._accumulator is None:
            raise Exception("no value in accumulator to get")
        return self._accumulator

    def clear_accumulator(self):
        # print("accumulator cleared")
        self._accumulator = None

    def read_input(self):
        return self._in.read()

    def write_output(self, value):
        self._out.write(value)

    def jump(self, target):
        if 0 <= target < len(self._program):
            self._code_pointer = target
        else:
            raise Exception("jump address out of bounds {}".format(target))

    def advance(self):
        self._code_pointer += 1
        if self._code_pointer >= len(self._program):
            self._code_pointer = 0

    def write(self, value, address):
        if 0 <= address.value < len(self._memory):
            self._memory[address.value] = value
        else:
            raise Exception("write out of bounds {} @ {}".format(value, address))

    def read(self, address):
        if 0 <= address.value < len(self._memory):
            return self._memory[address.value]
        else:
            raise Exception("read out of bounds {}".format(address))
