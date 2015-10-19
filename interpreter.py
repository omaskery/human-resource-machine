

import hrminterp
import argparse


def main():
    args = get_args()

    image = tuple(map(hrminterp.Value.parse, args.memory.read().split(",")))
    io_in, io_out = hrminterp.io.ConsoleInput(), hrminterp.io.ConsoleOutput()

    if args.input is not None:
        io_in = hrminterp.io.FileInput(args.input)
    if args.output is not None:
        io_out = hrminterp.io.FileOutput(args.output)

    parsed = hrminterp.parse_program(args.program)
    program = hrminterp.assemble_bytecode(parsed)

    machine = hrminterp.Machine(io_in, io_out, len(image))
    machine.fill_memory(image)
    machine.set_program(program)
    machine.run()


def get_args():
    parser = argparse.ArgumentParser(
        description="program to interpret programs from Human Resource Machine"
    )
    parser.add_argument(
        '-p', '--program', type=argparse.FileType(), help="path to the program source", required=True
    )
    parser.add_argument(
        '-m', '--memory', type=argparse.FileType(), help="path to the memory image", required=True
    )
    parser.add_argument(
        '-i', '--input', type=argparse.FileType(), help="optional file that specifies input stream"
    )
    parser.add_argument(
        '-o', '--output', type=argparse.FileType('w'), help="optional file to write output to"
    )
    return parser.parse_args()


if __name__ == "__main__":
    main()
