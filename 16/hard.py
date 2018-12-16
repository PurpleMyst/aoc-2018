import re

from easy import CPU


def main():
    shite = re.findall(
        r"Before: \[(.*?)\]\n(\d+) (\d+) (\d+) (\d+)\nAfter:  \[(.*?)\]",
        open("16/input.txt").read(),
    )

    opcodes = {}

    for before, opcode, a, b, c, after in shite:
        before = list(map(int, before.split(", ")))
        after = list(map(int, after.split(", ")))
        opcode = int(opcode)
        a = int(a)
        b = int(b)
        c = int(c)
        instructions = CPU.possible_instructions(before, after, a, b, c)
        opcodes.setdefault(opcode, set()).update(instructions)

    while opcodes:
        known = {k: v for k, v in opcodes.items() if len(v) == 1}

        for k, [v] in known.items():
            CPU.opcodes[k] = v
            for s in opcodes.values():
                s.discard(v)
            del opcodes[k]

    inp = open("16/input.txt").read()
    program = [
        map(int, l.split())
        for l in inp[inp.index("\n\n\n") + 3 :].splitlines()
        if l
    ]

    cpu = CPU()
    cpu.run(program)
    print(cpu.registers[0])


if __name__ == "__main__":
    main()
