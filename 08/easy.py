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

    def metadata_sum(self):
        return sum(self.metadata) + sum(c.metadata_sum() for c in self.children)


def main():
    numbers = map(int, open("08/input.txt").read().split(" "))
    print(Node.from_input(numbers).metadata_sum())


if __name__ == "__main__":
    main()
