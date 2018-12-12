def load_input():
    inp = open("12/input.txt")

    # Plants are stored in a set where each element that's present represents
    # the index of a plant.
    # You can test for existance of a plant, given its index, if its index is
    # in the set.
    plants = set()

    initial = next(inp).strip().split(": ")[1]
    next(inp)
    for i, c in enumerate(initial):
        if c == "#":
            plants.add(i)

    # We build a data-structure that's known as a "trie", a tree-based
    # data structure which allows for fast pattern-matching.
    trie = {}
    for line in inp:
        from_, to = line.strip().split(" => ")

        from_ = [c == "#" for c in from_]
        to = to == "#"

        curr = trie
        for c in from_[:-1]:
            next_ = curr.setdefault(c, {})
            curr = next_

        curr[from_[-1]] = to

    return plants, trie


def advance(plants, trie):
    # Only pots that have a plant within two spaces need to be considered.
    # The rule '..... => .' does not matter.
    viable = set()
    for plant in plants:
        viable.add(plant - 2)
        viable.add(plant - 1)
        viable.add(plant)
        viable.add(plant + 1)
        viable.add(plant + 2)

    new_plants = set()
    for plant in viable:
        curr = trie
        for off in range(-2, 2 + 1):
            try:
                curr = curr[(plant + off) in plants]
            except KeyError:
                # If we have no rule for this plant's neighborhood,
                # just leave it as-is.
                curr = plant in plants
                break

        if curr:
            new_plants.add(plant)

    return new_plants


def simulate(generations):
    plants, trie = load_input()

    for _ in range(generations):
        plants = advance(plants, trie)

    return sum(plants)


def main():
    print(simulate(20))


if __name__ == "__main__":
    main()
