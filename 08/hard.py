import dataclasses
import typing as t


@dataclasses.dataclass
class Node:
    children: t.List['Node']
    metadata: t.List[int]

    @classmethod
    def from_input(cls, inp):
        child_amount = next(inp)
        metadata_amount = next(inp)
        children = [cls.from_input(inp) for _ in range(child_amount)]
        metadata = [next(inp) for _ in range(metadata_amount)]
        return cls(children, metadata)

    def value(self):
        if self.children:
            values = [child.value() for child in self.children]
            indexes = [i - 1 for i in self.metadata if i != 0 and i <= len(self.children)]
            return sum(values[i] for i in indexes)
        else:
            return sum(self.metadata)


def main():
    numbers = map(int, open("08/input.txt").read().split(" "))
    print(Node.from_input(numbers).value())


if __name__ == "__main__":
    main()
