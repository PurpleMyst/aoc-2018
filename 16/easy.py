import re


class CPU:
    opcodes = {}

    def __init__(self, registers=[0, 0, 0, 0]):
        self.registers = registers[:]

    def addr(self, a, b, c):
        self.registers[c] = self.registers[a] + self.registers[b]

    def addi(self, a, b, c):
        self.registers[c] = self.registers[a] + b

    def mulr(self, a, b, c):
        self.registers[c] = self.registers[a] * self.registers[b]

    def muli(self, a, b, c):
        self.registers[c] = self.registers[a] * b

    def banr(self, a, b, c):
        self.registers[c] = self.registers[a] & self.registers[b]

    def bani(self, a, b, c):
        self.registers[c] = self.registers[a] & b

    def borr(self, a, b, c):
        self.registers[c] = self.registers[a] | self.registers[b]

    def bori(self, a, b, c):
        self.registers[c] = self.registers[a] | b

    def setr(self, a, _b, c):
        self.registers[c] = self.registers[a]

    def seti(self, a, _b, c):
        self.registers[c] = a

    def gtir(self, a, b, c):
        self.registers[c] = int(a > self.registers[b])

    def gtri(self, a, b, c):
        self.registers[c] = int(self.registers[a] > b)

    def gtrr(self, a, b, c):
        self.registers[c] = int(self.registers[a] > self.registers[b])

    def eqir(self, a, b, c):
        self.registers[c] = int(a == self.registers[b])

    def eqri(self, a, b, c):
        self.registers[c] = int(self.registers[a] == b)

    def eqrr(self, a, b, c):
        self.registers[c] = int(self.registers[a] == self.registers[b])

    instructions = (
        addr,
        addi,
        mulr,
        muli,
        banr,
        bani,
        borr,
        bori,
        setr,
        seti,
        gtir,
        gtri,
        gtrr,
        eqir,
        eqri,
        eqrr,
    )

    @classmethod
    def possible_instructions(cls, before, after, a, b, c):
        for instruction in cls.instructions:
            cpu = cls(before)
            instruction(cpu, a, b, c)
            if cpu.registers == after:
                yield instruction

    def run(self, program):
        for opcode, a, b, c in program:
            instruction = self.opcodes[opcode]
            instruction(self, a, b, c)


def main():
    shite = re.findall(
        r"Before: \[(.*?)\]\n\d+ (\d+) (\d+) (\d+)\nAfter:  \[(.*?)\]",
        open("16/input.txt").read(),
    )

    total = 0
    for before, a, b, c, after in shite:
        before = list(map(int, before.split(", ")))
        after = list(map(int, after.split(", ")))
        a = int(a)
        b = int(b)
        c = int(c)
        n = sum(1 for _ in CPU.possible_instructions(before, after, a, b, c))
        if n >= 3:
            total += 1

    print(total)


if __name__ == "__main__":
    main()
